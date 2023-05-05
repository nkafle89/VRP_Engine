from Problem import Problem
from RouteManager import RouteManager
from Customer import Customer
from typing import List
from Label import Label
from Resources import Resources
from Stop import Stop
from Route import Route


class ShortestPath:
    def __init__(self, problem: Problem, route_mgr: RouteManager, customer_subset: List[int], max_depth: int):
        self.problem = problem
        self.route_mgr = route_mgr
        self.myCustomers = customer_subset
        self.max_depth = max_depth
        self.user_max_depth = max_depth
        self.all_labels = []
        self.in_sub_iter = False

    def initialize(self):
        if not self.in_sub_iter:
            self.max_depth = self.user_max_depth
            self.connection_calculate()
            self.reset_labels()

    def get_positive_duals_only(self):
        self.myCustomers = [0]
        i: Customer
        for i in self.problem.customers.values():
            if i.dual > 0.01:
                self.myCustomers.append(i.cust_no)
        self.myCustomers.append(self.problem.total_customers - 1)

    def reset_labels(self):
        i: Customer
        for i in self.problem.customers.values():
            i.labels = []

    def reset_labels_cost(self):
        i: Customer
        j: Label
        for i in self.problem.customers.values():
            for j in i.labels:
                j.resource.cost = self.get_route_cost_with_dual(j)

    def connection_calculate(self):
        i: Customer
        j: Customer
        for i in self.problem.customers.values():
            for j in self.problem.customers.values():
                self.can_connect(i, j)

    def can_connect(self, first: Customer, second: Customer):
        if first == second:
            return
        if first.is_depot and second.is_depot:
            return
        if second.is_start_depot:
            return
        if first.is_end_depot:
            return

        inter_dist = self.problem.distances[first.cust_no, second.cust_no]
        if second.due_date > first.ready_time + first.service_time + inter_dist:
            first.can_connect_to[second] = inter_dist - first.dual
            return

    def spprc(self):
        self.all_labels = []
        c_node: Customer = self.problem.customers[0]
        assert c_node.is_start_depot, 'First Customer is not a depot'
        capacity = self.problem.vehicles.capacity
        initial_resource = Resources(capacity, c_node.ready_time + c_node.service_time, 0)

        initial_label = Label(initial_resource, c_node, [c_node])
        initial_label.initial = True
        c_node.labels.append(initial_label)
        self.all_labels.append(initial_label)

        while len(self.all_labels) > 0:
            l: Label = self.all_labels.pop(0)
            c_node = l.current_customer
            self.extend_label(l, c_node)

    def extend_label(self, label: Label, c_node: Customer):
        c_node_all_labels = c_node.labels

        for i in c_node_all_labels:
            if label.is_dominated(i):
                return

        can_goto = c_node.can_connect_to
        sort_can_goto = sorted(can_goto, key=lambda k: can_goto[k])

        limit = self.max_depth
        limit = min(limit, len(sort_can_goto))
        sort_can_goto = sort_can_goto[0:limit]

        c_cust: Customer = label.current_customer
        res: Resources = label.resource
        i: Customer
        for i in sort_can_goto:
            if i in label.vis_cust_set:
                continue
            inter_dist = self.problem.distances[c_cust.cust_no, i.cust_no]
            arrival = max(res.ready_time + inter_dist, i.ready_time)
            if arrival > i.due_date:
                continue
            rem_cap = res.capacity - i.demand
            if rem_cap < 0:
                continue

            cost = res.cost + can_goto[i]
            next_resource = Resources(rem_cap, arrival + i.service_time, cost)
            next_node: Customer = i
            next_visited = label.visited_customers + [i]
            next_label = Label(next_resource, next_node, next_visited)
            next_node.labels.append(next_label)
            self.all_labels.append(next_label)

    def get_route_cost_with_dual(self, label: Label):
        tot_custs = len(label.visited_customers)
        rt_cost = 0
        for i in range(tot_custs - 1):
            cust = label.visited_customers[i]
            next_cust = label.visited_customers[i+1]
            rt_cost += self.problem.distances[cust.cust_no, next_cust.cust_no] - cust.dual
        return rt_cost

    def get_routes(self):
        end_cust = self.problem.customers[self.problem.total_customers - 1]
        first_cust = self.problem.customers[0]

        for label in end_cust.labels:
            route = Route()
            stop = Stop(first_cust, 0, 0, 0)
            rt_dual_cost = self.get_route_cost_with_dual(label)

            if rt_dual_cost > -0.01:
                continue

            if not route.initialized:
                route.initialize()
            route.stops.append(stop)
            first_cust.customer_in_routes(route)

            for cust in label.visited_customers:
                if cust.cust_no == 0:
                    continue
                last_stop = route.stops[-1]
                dist = self.problem.distances[last_stop.customer.cust_no, cust.cust_no]
                stop = Stop(cust, 0, 0, 0)  # need to finalize the route with values for 0s.
                route.stops.append(stop)
                route.cost += dist
                cust.customer_in_routes(route)

            # if route.cost < 0.01:
            self.route_mgr.finalize_route(route)
