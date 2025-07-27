from distance_matrix import distance_matrix


def solve_vrp(data: VRPRequest):
    # Convert to OR-Tools format
    locations = data.locations
    demands = data.demands
    capacities = data.vehicle_capacities
    num_vehicles = data.num_vehicles
    depot_index = data.depot_index
    
    # Solve with constraints
    data_model = {
    "distance_matrix": distance_matrix(locations),
    "demands": demands,
    "vehicle_capacities": capacities,
    "num_vehicles": num_vehicles,
    "depot": depot_index
}
    routing, manager, solution = ortools_solver(data_model)
    
    # Return list of routes
    routes = get_routes(routing, manager, solution, data["num_vehicles"])
    return {"routes": routes}
