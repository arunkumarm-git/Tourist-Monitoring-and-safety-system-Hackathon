from shapely.geometry import Point, Polygon
from typing import Dict, List, Tuple
import json

def load_zones(zones_path: str) -> Dict:
    with open(zones_path, 'r') as f:
        return json.load(f)

def create_polygon(coords: List[Dict]) -> Polygon:
    return Polygon([(p["lng"], p["lat"]) for p in coords])

class ZoneDetector:
    def __init__(self, zones_path: str):
        self.zones = load_zones(zones_path)
        self.marina_polygon = create_polygon(self.zones["marina_boundary"])
        self.fishing_polygon = create_polygon(self.zones["fishing_area"])
        self.deep_water_polygon = create_polygon(self.zones["deep_water_zone"])
        self.attraction_centers = self.zones["attraction_centers"]
    
    def get_zone_type(self, lat: float, lng: float) -> str:
        point = Point(lng, lat)
        
        if self.deep_water_polygon.contains(point):
            return "deep_water"
        elif self.fishing_polygon.contains(point):
            return "fishing"
        elif self.marina_polygon.contains(point):
            return "safe"
        else:
            return "outside"
    
    def is_in_danger_zone(self, lat: float, lng: float) -> bool:
        return self.get_zone_type(lat, lng) == "deep_water"
    
    def is_in_restricted_zone(self, lat: float, lng: float) -> bool:
        return self.get_zone_type(lat, lng) == "fishing"
    
    def get_nearest_attraction(self, lat: float, lng: float) -> Tuple[Dict, float]:
        min_dist = float('inf')
        nearest = None
        
        for attraction in self.attraction_centers:
            dist = ((lat - attraction["lat"])**2 + (lng - attraction["lng"])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                nearest = attraction
        
        return nearest, min_dist
    
    def get_all_zones(self) -> Dict:
        return self.zones