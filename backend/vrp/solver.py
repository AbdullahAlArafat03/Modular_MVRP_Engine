from distance_matrix import create_distance_matrix


def solve_vrp(data: VRPRequest):
    # Convert to OR-Tools format
    locations =  [data.depot] + data.stops
    demands = [data.depot.demand] + [stop.demand for stop in data.stops]
    capacities = [v.capacity for v in data.vehicles]
    num_vehicles = data.num_vehicles
    depot_index = data.depot_index
    
    # Solve with constraints
    data_model = {
    "distance_matrix": create_distance_matrix(locations),
    "demands": demands,
    "vehicle_capacities": capacities,
    "num_vehicles": num_vehicles,
    "depot": depot_index
}
    routing, manager, solution = ortools_solver(data_model)
    
    # Return list of routes
    routes = get_routes(routing, manager, solution, data["num_vehicles"])
    return {"routes": routes}
