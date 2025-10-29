from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import uvicorn

from utils.dbscan import TouristClusterer
from utils.zone_detection import ZoneDetector
import config

app = FastAPI(title="T-MASS AI Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clusterer = TouristClusterer(
    epsilon_meters=config.EPSILON_METERS,
    min_samples=config.MIN_SAMPLES
)
zone_detector = ZoneDetector(zones_path=str(config.ZONES_PATH))

class TouristPosition(BaseModel):
    id: str
    lat: float
    lng: float
    speed_kmh: Optional[float] = 0.0
    status: Optional[str] = "active"

class AnalyzeRequest(BaseModel):
    tourists: List[TouristPosition]

class AnalyzeResponse(BaseModel):
    tourists: List[Dict]
    clusters: List[Dict]
    stats: Dict

@app.get("/")
def root():
    return {"service": "T-MASS AI Service", "status": "running", "version": "1.0.0"}

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_tourists(request: AnalyzeRequest):
    try:
        positions = [
            {
                "id": t.id,
                "lat": t.lat,
                "lng": t.lng,
                "speed_kmh": t.speed_kmh,
                "status": t.status
            }
            for t in request.tourists
        ]
        
        clustering_result = clusterer.cluster_positions(positions)
        
        for tourist in clustering_result["tourists"]:
            zone_type = zone_detector.get_zone_type(tourist["lat"], tourist["lng"])
            tourist["zone_type"] = zone_type
            tourist["in_danger"] = zone_type == "deep_water"
            tourist["in_restricted"] = zone_type == "fishing"
        
        return AnalyzeResponse(
            tourists=clustering_result["tourists"],
            clusters=clustering_result["clusters"],
            stats=clustering_result["stats"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cluster")
def cluster_only(request: AnalyzeRequest):
    try:
        positions = [{"id": t.id, "lat": t.lat, "lng": t.lng} for t in request.tourists]
        result = clusterer.cluster_positions(positions)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/zones")
def get_zones():
    return zone_detector.get_all_zones()

@app.get("/config")
def get_config():
    return {"epsilon_meters": config.EPSILON_METERS, "min_samples": config.MIN_SAMPLES}

if __name__ == "__main__":
    uvicorn.run("app:app", host=config.HOST, port=config.PORT, reload=config.DEBUG)
