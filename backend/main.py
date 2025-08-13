from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from vrp.models import VRPRequest, VRPResponse
from vrp.adapter import adapter
from vrp.emissions import estimate_emissions

app = FastAPI()


# use uvicorn's error logger
logger = logging.getLogger("uvicorn.error")

SENSITIVE_KEYS = {"api_key", "authorization", "apikey", "token"}

def redact(obj):
    if isinstance(obj, dict):
        return {k: ("***" if k.lower() in SENSITIVE_KEYS else redact(v)) for k, v in obj.items()}
    if isinstance(obj, list):
        return [redact(v) for v in obj]
    return obj

def has_none_or_nan(x):
    if x is None:
        return True
    try:
        return any((v is None) or (isinstance(v, float) and math.isnan(v)) for v in x)
    except TypeError:
        return False


# CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend is live"}

@app.post("/solve", response_model=VRPResponse)
def solve(data: VRPRequest):
    solution = adapter(data)
    emissions = estimate_emissions(solution)
    return {**solution, "co2": emissions}
