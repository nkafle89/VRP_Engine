class Vehicle:
    def __init__(self, capacity, number, _type=None):
        self.type = _type
        self.capacity = capacity
        self.number = number
        self.constraint = None
        self.variable = None
