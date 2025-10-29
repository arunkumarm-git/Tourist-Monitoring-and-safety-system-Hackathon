import time
from datetime import datetime

def get_current_timestamp():
    return int(time.time() * 1000)

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp / 1000).isoformat()

def calculate_distance(lat1, lng1, lat2, lng2):
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371000
    
    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)
    delta_lat = radians(lat2 - lat1)
    delta_lng = radians(lng2 - lng1)
    
    a = sin(delta_lat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lng/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c