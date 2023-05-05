from MasterProblem import MasterProblem
#from SubProblem_mip import SubProblem_mip
from ShortestPath import ShortestPath
import time


class ColGen:
    def __init__(self, num_iters, problem, routes_store, algo, sp_max_depth, sub_iters, ips):
        self.num_iters = num_iters
        self.problem = problem
        self.routes_store = routes_store
        self.MP = None
        self.SP = None
        self.stats = []
        self.algo = algo
        self.in_sub_iter = False
        self.sp_max_depth = sp_max_depth
        self.sub_iters = sub_iters
        self.final_solution = None
        self.final_mip_obj_val = -1
        self.final_lp_obj_val = -1
        self.veh_used = -1
        self.ips_stabilize = ips

    def run_algorithm(self):
        opt = False
        iterations = 0

        self.SP = ShortestPath(self.problem, self.routes_store, [], self.sp_max_depth)

        while not opt and iterations <= self.num_iters:
            self.MP = MasterProblem(self.problem, self.routes_store, self.ips_stabilize)
            self.MP.formulate_problem()
            # self.MP.write_lp("_lp_{0}.lp".format(iterations))
            self.MP.solve(lp_relaxed=True)
            obj = self.MP.model.objective_value
            self.MP.ips_stabilization()

            num_routes_i = len(self.routes_store.routes)
            difference = -1
            sp_time_s = time.time()
            for m in range(self.sub_iters + 2):
                if self.algo == 'MIP':
                    self.SP.change_objective()
                    # self.SP.write_lp("_sub_new_{0}.lp".format(iterations))
                    self.SP.solve()
                    break
                elif self.algo == 'SPPRC':
                    self.SP.initialize()
                    print("Solving SPPRC with max_depth", self.SP.max_depth)
                    self.SP.spprc()
                    self.SP.get_routes()
                    num_routes_a = len(self.routes_store.routes)
                    difference = num_routes_a - num_routes_i
                    if difference > 0:
                        self.SP.in_sub_iter = False
                        break
                    else:
                        print(
                            "Couldn't find good routes with max_depth of {0} at iteration {1}".format(self.SP.max_depth,
                                                                                                      iterations))

                        step = (self.problem.total_customers - self.SP.user_max_depth) / (self.sub_iters + 1)
                        self.SP.max_depth = int(self.SP.user_max_depth + (m + 1) * step + 1)
                        self.SP.in_sub_iter = True
                        # print("Increasing max_depth to {0}".format(self.SP.max_depth))

            num_routes_a = len(self.routes_store.routes)
            difference = num_routes_a - num_routes_i
            sp_time_e = time.time()

            print('SubProblem added {0} routes at iteration {1}'.format(difference, iterations))

            p_stats = [sp_time_e - sp_time_s, difference, obj]
            self.stats.append(obj)

            if num_routes_a == num_routes_i:
                opt = False
                break

            if iterations % 1 == 0:
                print('Number of iters completed: ', iterations)
                print('Obj: ', obj)

            iterations += 1
            # self.MP.print_solution()

        print('Num iterations: ', iterations)
        print('F Obj: ', obj)
        self.final_lp_obj_val = obj

        print("Now solving MIP")
        self.MP = MasterProblem(self.problem, self.routes_store, False)
        self.MP.mip = True
        self.MP.formulate_problem()
        #self.MP.model.write('_lpfinal.lp')
        self.MP.solve(lp_relaxed=False)
        self.final_solution = self.MP.print_solution()
        self.final_mip_obj_val = self.MP.model.objective_value
        self.veh_used = len(self.final_solution)
        print('Final Obj: ', self.MP.model.objective_value)
