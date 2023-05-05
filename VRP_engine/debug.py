from Stop import Stop
import pandas as pd
import glob
import json


def read_file(filename):
    m1 = xp.problem()
    m1.read(filename)
    m1.solve()


def check_duplicate_routes(routes):
    for i in routes:
        for j in routes:
            if i != j:
                if routes[i].cost == routes[j].cost:
                    print("Possible duplicates", i, j)


def print_routes(routes, num):
    cus_list = []
    for i in routes.routes[num].stops:
        cus_list.append(i.customer.cust_no)
    print(cus_list)


def verify_solution(problem, selected_route):
    capacity = 0
    for i in selected_route:
        capacity += problem.customers[i].demand
    print('Load: ', capacity)
    if capacity > problem.vehicles.capacity:
        print('Error, Capacity exceeded')
        return

    dist = 0
    last_depart = problem.customers[0].ready_time
    for i in range(len(selected_route) - 1):
        curr = selected_route[i]
        nextc = selected_route[i + 1]
        two_dist = problem.distances[curr, nextc]
        dist += two_dist

        arrival = max(last_depart + two_dist, problem.customers[nextc].ready_time)
        if arrival > problem.customers[nextc].due_date:
            print('Error, arrival time at customer {0} exceeded'.format(nextc))
            return
        last_depart = arrival + problem.customers[nextc].service_time

    print('Dist', dist)
    return dist


def total_cost(myProblem, optimal):
    total_dist = 0
    for i in optimal:
        total_dist += verify_solution(myProblem, i)
    print('Total Cost is ', total_dist)
    return total_dist


def flat_list(selected):
    return [item for sublist in selected for item in sublist]


def get_plain_solution(solution, problem):
    cust_no = 0
    rte = [0]
    cost = 0
    stop = False
    while not stop:
        for i in solution[cust_no]:
            if solution[cust_no][i] > 0.5:
                dist = problem.distances[cust_no, i]
                rte.append(i)
                cost += dist
                cust_no = i

                if i == 0:
                    stop = True
                    break
                break
    return rte


def get_route_cost_with_dual(problem, rte, dual):
    tot_custs = len(rte)
    rt_cost = 0
    for i in range(tot_custs - 1):
        cust = rte[i]
        next_cust = rte[i + 1]
        customer = problem.customers[cust]
        if dual:
            rt_cost += problem.distances[cust, next_cust] - customer.dual
        else:
            rt_cost += problem.distances[cust, next_cust]
    return rt_cost


def compare_solutions(input_folder):
    #input_folder = '../results_no_ips/*'
    benchmark = pd.read_csv(r'../results/Benchmark_solutions.csv')
    benchmark.Problem = benchmark.Problem.str.upper()

    myResult = glob.glob(input_folder)
    myResult = [i for i in myResult if not i.endswith('.csv')]

    rows = []
    for i in myResult:
        f = open(i)
        data = json.load(f)
        rows.append([data['Problem'], data['vehicles'], data['mip_obj'], data['lp_obj'], len(data['stats']), data['total_time']])

    col_names = ['Problem', 'Vehicles_cg', 'Distance_cg', 'LP_value_cg', 'Iterations', 'time_cg']
    result_df = pd.DataFrame(rows, columns=col_names)

    new_df = pd.merge(result_df, benchmark, on='Problem', how='left')
    new_df = new_df.sort_values(by=['Problem'])

    new_df['Ratio'] = new_df['Distance']/new_df['Distance_cg']

    return new_df


df = compare_solutions('../results_no_ips/*')
df.to_csv('../ResultComparision/no_ips.csv')
