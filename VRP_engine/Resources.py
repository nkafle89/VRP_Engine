import numpy as np


class Resources:
    def __init__(self, capacity: int, ready_time: int, cost: int):
        self.capacity = capacity
        self.ready_time = ready_time
        self.cost = cost
