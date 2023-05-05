class Stop:
    def __init__(self, customer, arrive, depart, rem_load):
        self.customer = customer
        self.arrive = arrive
        self.depart = depart
        self.action = 'Drop'
        self.remaining_load = rem_load
