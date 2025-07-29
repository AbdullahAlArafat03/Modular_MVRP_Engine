from geo.distance_matrix import create_distance_matrix
from vrp.core_solver import ortools_solver, get_routes
from vrp.models import VRPRequest


def solve_vrp(data: VRPRequest):
    # Convert to OR-Tools format
    locations =  [data.depot] + data.stops
    demands = [data.depot.demand] + [stop.demand for stop in data.stops]
    capacities = [v.capacity for v in data.vehicles]
    num_vehicles = len(data.vehicles)
    depot_index = 0
    API_key = data.api_key
    
    # Solve with constraints
    data_model = {
    "distance_matrix": create_distance_matrix(locations, API_key),
    "demands": demands,
    "vehicle_capacities": capacities,
    "num_vehicles": num_vehicles,
    "depot": depot_index
}
    routing, manager, solution = ortools_solver(data_model)
    
    # Return list of routes
    routes = get_routes(routing, manager, solution, num_vehicles)
    return {"routes": routes}
