class Customer:
    def __init__(self, cust_prop):
        self.labels = []
        self.cust_no = cust_prop[0]
        self.x_cord = cust_prop[1]
        self.y_cord = cust_prop[2]
        self.demand = cust_prop[3]
        self.ready_time = cust_prop[4]
        self.due_date = cust_prop[5]
        self.service_time = cust_prop[6]
        self.is_depot = False
        self.is_start_depot = False
        self.is_end_depot = False
        self.in_routes = []
        self.constraint = None
        self.dual = 0
        self.uncover_var = None
        self.can_connect_to = {}
        self.node = None
        self.ips_dual_vector = []

    def customer_in_routes(self, route):
        self.in_routes.append(route.route_id)

    def __lt__(self, other):
        return self.due_date < other.due_date

    def __gt__(self, other):
        return self.due_date > other.due_date

    def __le__(self, other):
        return self.due_date <= other.due_date

    def __ge__(self, other):
        return self.due_date >= other.due_date

    def __repr__(self):
        return "Customer_{0}".format(self.cust_no)

    def __str__(self):
        return "Customer_{0}".format(self.cust_no)
