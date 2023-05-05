import math
from Vehicle import Vehicle
from Customer import Customer


class Problem:
    def __init__(self, filename):
        self.filename = filename
        self.problem_id = ''
        self.vehicles = None
        self.customers = {}
        self.distances = {}
        self.total_customers = 0

    def read_file(self, mode='r'):
        myline = 0
        with open(self.filename, mode=mode) as f:
            first_depot = None
            for line in f:
                myline += 1

                if myline == 1:
                    self.problem_id = line.strip()

                if myline == 5:
                    info = " ".join(line.split()).split(' ')
                    info = [int(x) for x in info]
                    self.vehicles = Vehicle(number=info[0], capacity=info[1])

                if myline >= 10:
                    info = " ".join(line.split()).split(' ')
                    info = [int(x) for x in info]
                    self.customers[info[0]] = Customer(info)

                    if first_depot is None:
                        self.customers[info[0]].is_depot = True
                        self.customers[info[0]].is_start_depot = True
                        first_depot = info

        include_last_depot = True
        if include_last_depot:
            # replicate first depot and end depot
            total_customers = len(self.customers)
            first_depot[0] = total_customers
            self.customers[first_depot[0]] = Customer(first_depot)
            self.customers[first_depot[0]].is_depot = True
            self.customers[first_depot[0]].is_end_depot = True
        self.total_customers = len(self.customers)

    def calculate_distances(self):
        for i in self.customers:
            for j in self.customers:
                if i != j:
                    self.distances[i, j] = self.distance(self.customers.get(i), self.customers.get(j))

    def initialize(self):
        self.read_file()
        self.calculate_distances()

    @staticmethod
    def distance(cust_i, cust_j):
        return round(math.sqrt((cust_i.x_cord - cust_j.x_cord) ** 2 +
                               (cust_i.y_cord - cust_j.y_cord) ** 2), 3)


if __name__ == '__main__':
    myProblem = Problem('../data/c101.txt')
    myProblem.initialize()
