import os
from dotenv import load_dotenv
from vrp.models import VRPRequest, Location, Vehicle
from vrp.adapter import adapter

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Create test data
request_data = VRPRequest(
    depot=Location(id="depot", coordinates=(40.7580, -73.9855), time_window=(0, 1000), demand=0),
    start_depots = [0,0],
    end_depots = [0,0],
    stops=[
        Location(id="A", coordinates=(40.730610, -73.935242), time_window=(0, 1000), demand=5),
        Location(id="B", coordinates=(40.712776, -74.005974), time_window=(0, 1000), demand=3),
        Location(id="C", coordinates=(40.706192, -74.009160), time_window=(0, 1000), demand=2),
        Location(id="D", coordinates=(40.748817, -73.985428), time_window=(0, 1000), demand=4)
    ],
    vehicles=[
        Vehicle(id="v1", capacity=10, type="van", cost_per_km=1.0, fixed_cost=100.0),
        Vehicle(id="v2", capacity=12, type="truck",  cost_per_km=2.0, fixed_cost=150.0)
    ],
    api_key= API_KEY
)

solution = adapter(request_data)

print("Step 1: Preparing data model...")
print(data_model)

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
co2_estimate = estimate_emissions(solution)
print(f"\nEstimated CO₂: {co2_estimate} kg")
