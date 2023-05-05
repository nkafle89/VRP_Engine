from Problem import Problem
from RouteManager import RouteManager
from ColGen import ColGen
from Results import Result
import glob
import time
import os
from Route import Route


if __name__ == '__main__':
    all_cases = glob.glob('../data/100_customers/c_cases/c104*')
    AllResults = []

    for i in all_cases:
        s_time = time.time()
        print("Solving", i)
        myProblem = Problem(i)
        myProblem.initialize()

        result_loc = '../results/'
        result_file = result_loc + myProblem.problem_id
        if os.path.isfile(result_file):
            pass
            #continue

        RS = RouteManager()
        RS.singleton_routes(myProblem)
        RS.initial_solution(myProblem)

        colgen = ColGen(1000, myProblem, RS, 'SPPRC', 11, 5, True)
        colgen.run_algorithm()

        e_time = time.time()
        t_time = e_time - s_time

        result = Result(myProblem.problem_id, colgen.stats, colgen.veh_used, colgen.final_solution,
                        colgen.final_mip_obj_val, colgen.final_lp_obj_val, t_time)
        result.write_to_file(result_loc)
        AllResults.append(result)
        #additional process for running in loop. Reset my_id
        Route.my_id = 0

    #pickle_file = open('allresults', 'wb')
    #pickle.dump(AllResults, pickle_file)
    #pickle_file.close()
