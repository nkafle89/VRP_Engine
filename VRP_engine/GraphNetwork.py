import networkx as nx


class NetworkGraph:
    def __init__(self, problem, route_store):
        self.problem = problem
        self.route_store = route_store
        self.graph = nx.Graph

    def add_edges(self):
        for i in self.problem.customers.items():
            self.graph.add_node(i.cust_no)

        for i in self.problem.customers.values():
            for j in self.problem.customers.values():
                if i != j:
                    if i.ready_time + self.problem.distances[i.cust_no, j.cust_no] > j.due_date:
                        continue

                    dist = self.problem.distances[i.cust_no, j.cust_no]
                    self.graph.add_edge(i.cust_no, j.cust_no, distance=dist)

