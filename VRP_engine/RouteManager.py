from Route import Route
from Stop import Stop


class RouteManager:
    def __init__(self):
        self.routes = {}
        self.initial_routes = [None] * 2  # [start_index, end_index] for initial routes
        self.routes_identifier = {}

    def singleton_routes(self, problem):
        depot_cus = problem.customers[0]
        depot = Stop(depot_cus, depot_cus.ready_time, depot_cus.ready_time + depot_cus.service_time,
                     problem.vehicles.capacity)
        end_cus = problem.customers[problem.total_customers - 1]
        end_depot = Stop(end_cus, end_cus.ready_time, end_cus.ready_time + end_cus.service_time,
                         problem.vehicles.capacity)

        for num, cust in problem.customers.items():
            if num == 0:
                continue
            if num == problem.total_customers - 1:
                continue

            route = Route()
            route.stops.append(depot)
            if not route.initialized:
                route.initialize()
            next_stop = Stop(cust, 0, 0, 0)
            route.stops.append(next_stop)
            dist = problem.distances[0, num]

            if cust.ready_time < dist:
                cust.ready_time = dist

            route.cost += dist
            route.stops.append(end_depot)
            dist = problem.distances[num, end_cus.cust_no]
            route.cost += dist

            cust.customer_in_routes(route)
            self.finalize_route(route)

    def initial_solution(self, problem):
        self.initial_routes[0] = len(self.routes)
        visited = []
        cust_list = list(problem.customers.values())
        depot_cust = cust_list[0]
        cust_list = cust_list[1:-1]
        cust_list.sort()

        for i in range(problem.vehicles.number):

            if len(visited) == len(cust_list):
                self.initial_routes[1] = len(self.routes)
                return

            depot = Stop(depot_cust, depot_cust.ready_time, depot_cust.ready_time + depot_cust.service_time,
                         problem.vehicles.capacity)
            route = Route()
            route.stops.append(depot)

            for cust in cust_list:
                if cust.cust_no not in visited:
                    last_stop = route.stops[-1]
                    dist = problem.distances[last_stop.customer.cust_no, cust.cust_no]
                    if last_stop.depart + dist <= cust.due_date:
                        if cust.demand <= last_stop.remaining_load:
                            arrival = max(last_stop.depart + dist, cust.ready_time)
                            depart = arrival + cust.service_time
                            rem_load = last_stop.remaining_load - cust.demand
                            next_stop = Stop(cust, arrival, depart, rem_load)

                            if not route.initialized:
                                route.initialize()

                            route.stops.append(next_stop)
                            route.cost += dist
                            visited.append(cust.cust_no)

                            cust.customer_in_routes(route)

            last_stop = route.stops[-1]
            cust = problem.customers[problem.total_customers - 1]
            depot = Stop(cust, cust.ready_time, cust.ready_time + cust.service_time, problem.vehicles.capacity)
            route.stops.append(depot)
            dist = problem.distances[last_stop.customer.cust_no, 0]
            route.cost += dist
            self.finalize_route(route)

    def finalize_route(self, route):
        rt_list = [st.customer.cust_no for st in route.stops]
        rt_list = tuple(rt_list)

        if rt_list in self.routes_identifier:
            for i in route.stops:
                if route.route_id in i.customer.in_routes:
                    i.customer.in_routes.remove(route.route_id)
            Route.my_id -= 1
            return

        self.routes[route.route_id] = route
        self.routes_identifier[rt_list] = route.route_id

    def __customer_in_route(self, unused=True):
        for num, route in self.routes:
            for stop in route.stops:
                stop.customer.in_routes.append(num)
