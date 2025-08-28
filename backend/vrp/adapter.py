import os
from config import API_KEY
from distance_matrix import create_distance_matrix
from core_solver import ortools_solver, get_routes
from dotenv import load_dotenv
from models import VRPRequest

load_dotenv()
API_key = os.getenv("API_KEY")

def adapter(data: VRPRequest):
    # Convert to OR-Tools format
    locations =  [data.depot] + data.stops
    demands = [data.depot.demand] + [stop.demand for stop in data.stops]
    capacities = [v.capacity for v in data.vehicles]
    num_vehicles = len(data.vehicles)
    vehicle_time_limits = data.vehicles * 60
    depot_start_index = data.start_depots
    depot_end_index = data.end_depots

    dist_m = create_distance_matrix(locations, API_key)
    time_m = [[int(d / 1000) for d in row] for row in dist_m]

    
    
    # Solve with constraints
    data_model = {
    "distance_matrix": dist_m,
    "time_matrix": time_m,
    "demands": demands,
    "vehicle_capacities": capacities,
    "num_vehicles": num_vehicles,
    "vehicle_time_limits": vehicle_time_limits,
    "start_depots": data.start_depots,
    "end_depots": data.end_depots

}
    print("✅ Sending this to ortools_solver:")
    print(data_model.keys())  # or json.dumps(data_model, indent=2) if serializable
    
    routing, manager, solution = ortools_solver(data_model)

    print("✅ Done")
    
    # Return list of routes
    routes = get_routes(routing, manager, solution, num_vehicles)
    return {"routes": routes}
