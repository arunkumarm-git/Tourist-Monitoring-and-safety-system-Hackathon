import json
import random
import uuid
from datetime import datetime, timedelta

TOURIST_COUNT = 500
TIMESTAMP_COUNT = 25
INTERVAL_SECONDS = 10

CARNIVAL_CENTER = (13.06165, 80.28493)
FOOD_COURT_CENTER = (13.05626, 80.28446)
LIGHTHOUSE_CENTER = (13.03963, 80.27944)

def generate_position_near(center, radius_deg=0.001):
    lat_offset = random.uniform(-radius_deg, radius_deg)
    lng_offset = random.uniform(-radius_deg, radius_deg)
    return (center[0] + lat_offset, center[1] + lng_offset)

def generate_tourist_data():
    tourists = []
    
    for i in range(TOURIST_COUNT - 1):
        tourist_id = f"tourist_{str(uuid.uuid4())[:8]}"
        tourist_type = random.choice(['sunbather', 'explorer', 'active', 'family'])
        
        if tourist_type == 'sunbather':
            base_pos = generate_position_near(FOOD_COURT_CENTER, 0.002)
        elif tourist_type == 'explorer':
            base_pos = generate_position_near(CARNIVAL_CENTER, 0.003)
        elif tourist_type == 'family':
            base_pos = generate_position_near(LIGHTHOUSE_CENTER, 0.0015)
        else:
            base_pos = generate_position_near(CARNIVAL_CENTER, 0.004)
        
        positions = []
        current_pos = base_pos
        
        for t in range(TIMESTAMP_COUNT):
            timestamp = t * INTERVAL_SECONDS
            
            if tourist_type == 'sunbather':
                movement = random.uniform(0, 0.0001)
            elif tourist_type == 'explorer':
                movement = random.uniform(0.0002, 0.0005)
            else:
                movement = random.uniform(0.0001, 0.0003)
            
            lat = current_pos[0] + random.uniform(-movement, movement)
            lng = current_pos[1] + random.uniform(-movement, movement)
            current_pos = (lat, lng)
            
            positions.append({
                'timestamp': timestamp,
                'lat': round(lat, 6),
                'lng': round(lng, 6),
                'speed': round(random.uniform(0, 5), 2),
                'status': 'active',
                'current_zone': 'safe'
            })
        
        tourists.append({
            'tourist_id': tourist_id,
            'tourist_type': tourist_type,
            'positions': positions
        })
    
    mr_x_positions = []
    for t in range(TIMESTAMP_COUNT):
        timestamp = t * INTERVAL_SECONDS
        
        if t < 6:
            pos = generate_position_near(CARNIVAL_CENTER, 0.0005)
            status = 'active'
        elif t < 10:
            pos = (13.06165 + (t-6)*0.001, 80.28493 + (t-6)*0.0008)
            status = 'active'
        elif t < 14:
            pos = (13.06565, 80.28893 + (t-10)*0.0005)
            status = 'warning'
        elif t < 18:
            pos = (13.06465, 80.29193 + (t-14)*0.0003)
            status = 'warning'
        else:
            pos = (13.06365, 80.29393 + (t-18)*0.0002)
            status = 'critical'
        
        mr_x_positions.append({
            'timestamp': timestamp,
            'lat': round(pos[0], 6),
            'lng': round(pos[1], 6),
            'speed': round(random.uniform(2, 8), 2),
            'status': status,
            'current_zone': 'deep_water' if t >= 18 else ('fishing' if t >= 10 else 'safe')
        })
    
    tourists.append({
        'tourist_id': 'mr_x',
        'tourist_type': 'anomaly',
        'positions': mr_x_positions
    })
    
    return {
        'metadata': {
            'total_tourists': TOURIST_COUNT,
            'timestamps': TIMESTAMP_COUNT,
            'interval_seconds': INTERVAL_SECONDS,
            'generated_at': datetime.utcnow().isoformat()
        },
        'tourists': tourists
    }

if __name__ == '__main__':
    data = generate_tourist_data()
    with open('output/marina_beach_tourists_v2.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Generated data for {TOURIST_COUNT} tourists with {TIMESTAMP_COUNT} timestamps")