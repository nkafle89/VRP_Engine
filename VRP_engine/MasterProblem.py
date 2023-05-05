from docplex.mp.model import Model
import random
from Customer import Customer


class MasterProblem:
    def __init__(self, problem, route_store, ips):
        self.problem = problem
        self.model = Model(name='Master', log_output='False')
        self.route_store = route_store
        self.mip = False
        self.ips_stabilize = ips
        self.cov_cons = []

    def add_variables(self):
        for num, route in self.route_store.routes.items():
            if self.mip:
                route.variable = self.model.binary_var(name="Rt_{0}".format(num))
            else:
                route.variable = self.model.continuous_var(name="Rt_{0}".format(num))

    def set_objective(self):
        self.model.minimize(self.model.sum(route.variable * route.cost for route in self.route_store.routes.values()))

    def coverage_constraint(self):
        for cust in self.problem.customers.values():
            if cust.is_depot:
                continue

            cust.constraint = self.model.sum(self.route_store.routes[x].variable for x in cust.in_routes) >= 1
            cust.constraint.name = 'Cust_{0}'.format(cust.cust_no)
            self.cov_cons.append(cust.constraint)

        self.model.add_constraints(self.cov_cons)

    def vehicle_constraint(self):
        self.problem.vehicles.constraint = self.model.sum(x.variable for x in self.route_store.routes.values()) <= self.problem.vehicles.number
        self.problem.vehicles.constraint.name = 'Vehicles'
        self.model.add_constraint(self.problem.vehicles.constraint)

    def write_lp(self, filename=None):
        if filename is None:
            filename = '_lp.lp'
        self.model.export_as_lp(basename=filename)

    def solve(self, lp_relaxed=False):
        self.model.solve()
        if lp_relaxed:
            for i in self.problem.customers.values():
                if i.constraint is not None:
                    i.dual = self.model._dual_value1(i.constraint)

    def formulate_problem(self):
        self.add_variables()
        self.set_objective()
        self.coverage_constraint()

    def getAllSolComponents(self):
        x = self.model.solution._get_all_values()
        slack = self.model.slack_values(self.cov_cons)
        dual = self.model.dual_values(self.cov_cons)
        dj = self.model.reduced_costs([x.variable for x in self.route_store.routes.values()])
        return x, slack, dual, dj

    def print_solution(self):
        solution = self.model.solution._get_all_values()
        selected = [i for i in range(len(solution)) if solution[i] > 0.5]

        selected_rts = []
        for i in selected:
            rte = []
            for j in self.route_store.routes[i].stops:
                rte.append(j.customer.cust_no)
            selected_rts.append(rte)
            print(i, rte)
        return selected

    def ips_stabilization(self):
        if not self.ips_stabilize:
            return

        random.seed(a=1)
        x, slack, dual, df = self.getAllSolComponents()
        for i in range(len(dual)):
            self.problem.customers[i + 1].dual = 0

        R_star = [i for i in range(len(x)) if x[i] > 0]  # r for which x_r>
        Not_R_star = [i for i in range(len(x)) if x[i] <= 0]
        C = [i for i in range(len(slack)) if
             slack[i] > 0]  # C for which covering constraint is not tight or has non zero slack
        Not_C = [i for i in range(len(slack)) if slack[i] <= 0]
        # solve 20 times by changing RHS and variables bound

        dual_vec = []
        for num in range(20):
            u = [random.random() for i in range(self.problem.total_customers)]

            #not_c_rhs = [u[i] for i in Not_C]
            for k in Not_C:
                self.cov_cons[k].rhs = u[k]

            for k in C:
                self.cov_cons[k].rhs = -self.model.infinity

            for k in R_star:
                self.route_store.routes[k].variable.lb = -self.model.infinity

            for k in Not_R_star:
                self.route_store.routes[k].variable.lb = 0

            self.model.solve()

            x_p, slack_p, dual_p, df_p = self.getAllSolComponents()
            dual_vec.append(dual_p)

        avg_duals = [sum(x) / len(x) for x in zip(*dual_vec)]

        for ind, x in enumerate(avg_duals):
            self.problem.customers[ind + 1].dual = x

        print('Duals updated')
