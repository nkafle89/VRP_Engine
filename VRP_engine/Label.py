from Resources import Resources
from Customer import Customer
from typing import List
import numpy as np


class Label:
    def __init__(self, resource: Resources, current_customer: Customer, visited_customers: List[Customer]):
        self.resource = resource
        self.visited_customers = visited_customers
        self.current_customer = current_customer
        self.initial = False
        self.vis_cust_set = set(visited_customers)

    def is_dominated(self, other):
        if self == other:
            return False
        if self.initial:
            return False

        self_resource = self.resource
        other_resource = other.resource

        if other_resource.cost > self_resource.cost:
            return False
        if other_resource.ready_time > self_resource.ready_time:
            return False
        return True

    def __repr__(self):
        mystr = ""
        num_items = len(self.visited_customers)
        for i in range(num_items):
            if i == num_items - 1:
                mystr += str(self.visited_customers[i].cust_no)
            else:
                mystr += str(self.visited_customers[i].cust_no) + '->'
        return mystr

    def __str__(self):
        mystr = ""
        num_items = len(self.visited_customers)
        for i in range(num_items):
            if i == num_items - 1:
                mystr += str(self.visited_customers[i].cust_no)
            else:
                mystr += str(self.visited_customers[i].cust_no) + '->'
        return mystr