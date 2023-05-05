from Problem import Problem


class Route:
    my_id = 0

    def __init__(self):
        self.stops = []
        self.route_id = -1
        self.initialized = False
        self.variable = None
        self.cost = 0
        self.reduced_cost = 0
        self.length = 0
        self.total_load = 0

    def initialize(self):
        self.route_id = Route.my_id
        Route.my_id += 1
        self.initialized = True

    def __repr__(self):
        mystr = ""
        num_items = len(self.stops)
        for i in range(num_items):
            if i == num_items - 1:
                mystr += str(self.stops[i].customer.cust_no)
            else:
                mystr += str(self.stops[i].customer.cust_no) + '->'
        return mystr

    def __str__(self):
        mystr = ""
        num_items = len(self.stops)
        for i in range(num_items):
            if i == num_items - 1:
                mystr += str(self.stops[i].customer.cust_no)
            else:
                mystr += str(self.stops[i].customer.cust_no) + '->'
        return mystr

    def calculate_reduced_cost(self):
        lambdas = [i.customer.dual for i in self.stops]
        self.reduced_cost = self.cost - sum(lambdas)
