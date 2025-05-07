from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow requests from your frontend domain (or '*' during dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with actual origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EstimateRequest(BaseModel):
    miles: float
    origin: str
    destination: str

@app.post("/estimate")
def estimate(data: EstimateRequest):
    # Business logic
    fuel_perc = 0.30
    miles = max(data.miles, 800)
    estimate = round((miles * 1.8) + (miles * fuel_perc), 0)

    if (data.origin == "USA" and data.destination == "CA") or (data.origin == "CA" and data.destination == "USA"):
        estimate += 400

    currency = "USD" if data.origin == "USA" else "CAD"
    ppm = round(estimate / miles, 2)

    return {
        "estimate": estimate,
        "currency": currency,
        "miles": miles,
        "ppm": ppm
    }
