This repo has the implementation of Column Generation algorithm implementation for Vehicle Routing Problem with Time Windows. Users can clone the repo and solve the Solomon's benchmark problem for 100 customers (https://www.sintef.no/projectweb/top/vrptw/100-customers/). Details about the algorithm can be found in the following blog article (https://nabinkafle.medium.com/column-generation-for-solving-vrptw-a1dff766680e).

# Steps to run 
1. Clone the repo
2. Install the required packages
3. The code has dependency on CPLEX solver, so CPLEX should be pre installed on the system to run it.
4. Go to main.py inside VRP_Engine folder
5. Run main.py. If you want to solve only a specific scenario, specify the scenario in line 12 of the main.py
6. Results and comparison will be stored in results folder
