from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

# Define the decision variables
x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')

# Add constraints
ct = solver.Constraint(0, 160, 'ct')
ct.SetCoefficient(x1, 3)
ct.SetCoefficient(x2, 2)
ct = solver.Constraint(0, 200, 'ct')
ct.SetCoefficient(x1, 1)
ct.SetCoefficient(x2, 3)

# Set the profit as the objective function
objective = solver.Objective()
objective.SetCoefficient(x1, 5)
objective.SetCoefficient(x2, 12)
objective.SetMaximization()

# Solve the optimization problem
solver.Solve()

# print the results
print('LP Solution:')
print('Profit =', round(objective.Value(),2),'$')
print('Make', '%.1f'%round(x1.solution_value()),'small sets, and', '%.1f'%round(x2.solution_value()), 'large sets')
