import os, sys
from dotenv import load_dotenv
from models import VRPRequest, Location, Vehicle
from adapter import adapter
from core_solver import create_data_model
from core_solver import get_distance_km
from core_solver import get_routes
import json, sys, traceback



print("Loaded:", os.path.abspath(__file__), "__name__ =", __name__, flush=True)

load_dotenv()
API_key = os.getenv("API_KEY")


# Create test data
request_data = VRPRequest(
    create_data_model
)


solution = adapter(request_data)
get_routes(routing, manager, solution, num_vehicles)

total_km = get_distance_km(routes, data)

print("Step 1: Preparing data model...")
print(request_data)

# Benchmarking Module

    #  |
    #  |
    #  |
    #  V



# Routes
if solution.get("routes"):
    for idx, route in enumerate(solution["routes"]):
        print(f"Vehicle {idx + 1} route: {route}")
else:
    print("No routes found.")


# Total Cost
print(f"\nTotal Cost: {routing.GetCost(solution)}")

# Time per Vehicle
time_dimension = routing.GetDimensionOrDie("Time")
total_cost = routing.GetCost(solution)
for vehicle_id in range(num_vehicles):
    start_index = routing.Start(vehicle_id)
    end_index = routing.End(vehicle_id)

    start_time = solution.Value(time_dimension.CumlVar(start_index))
    end_time = solution.Value(time_dimension.CumlVar(end_index))
print(f"\nTime per Vehicle: {end_time - start_time} minutes")

# Estimated CO2
co2_estimate = estimate_emissions(total_km)
print(f"\nEstimated CO₂: {co2_estimate} kg")
