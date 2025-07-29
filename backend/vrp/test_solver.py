from vrp.models import VRPRequest, Location, Vehicle
from vrp.solver import solve_vrp

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("API_KEY")

# Create test data
request_data = VRPRequest(
    depot=Location(id="depot", coordinates=(40.7580, -73.9855), demand=0),
    stops=[
        Location(id="A", coordinates=(40.730610, -73.935242), demand=5),
        Location(id="B", coordinates=(40.712776, -74.005974), demand=3),
        Location(id="C", coordinates=(40.706192, -74.009160), demand=2),
        Location(id="D", coordinates=(40.748817, -73.985428), demand=4)
    ],
    vehicles=[
        Vehicle(id="v1", capacity=10, type="van"),
        Vehicle(id="v2", capacity=12, type="truck")
    ]
)

# Run the solver
solution = solve_vrp(request_data, api_key=API_KEY)

# Print routes
for idx, route in enumerate(solution["routes"]):
    print(f"Vehicle {idx + 1} route: {route}")

# Print emissions
if "co2" in solution:
    print(f"\nEstimated CO₂: {solution['co2']} kg")
