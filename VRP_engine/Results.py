import json


class Result:
    def __init__(self, problem_name, stats, vehicles, solution, mip_obj, lp_obj, total_time):
        self.result = {}
        self.result['Problem'] = problem_name
        self.result['stats'] = stats
        self.result['vehicles'] = vehicles
        self.result['solution'] = solution
        self.result['mip_obj'] = mip_obj
        self.result['lp_obj'] = lp_obj
        self.result['total_time'] = total_time

    def write_to_file(self, fileloc):
        filename = fileloc + self.result['Problem']
        with open(filename, 'w') as outfile:
            json.dump(self.result, outfile)


