import json, logging, math
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from vrp.models import VRPRequest, VRPResponse
from vrp.core_solver import ortools_solver
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

raw = await request.json()
logger.info("RAW BODY -> %s", json.dumps(redact(raw), ensure_ascii=False, indent=2))

depot = raw.get("depot", {})
if has_none_or_nan((depot.get("coordinates") or [None, None])) \
    or has_none_or_nan((depot.get("time_window") or [None, None])):
    raise HTTPException(status_code=422, detail="Depot fields must be numbers: coordinates[2], time_window[2].")

for i, s in enumerate(raw.get("stops", [])):
    if has_none_or_nan((s.get("coordinates") or [None, None])) \
        or has_none_or_nan((s.get("time_window") or [None, None])):
        raise HTTPException(status_code=422, detail=f"Stop {i} fields must be numbers: coordinates[2], time_window[2].")
data = VRPRequest(**raw)


def solve(data: VRPRequest):
    solution = ortools_solver(data)
    emissions = estimate_emissions(solution)
    return {**solution, "co2": emissions}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)