import json
import time
import firebase_admin
from firebase_admin import credentials, db
import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
FIREBASE_CREDS_PATH = os.path.join(script_dir, 'firebase-creds.json')
DATA_FILE = os.path.join(script_dir, 'output', 'marina_beach_tourists_v2.json')

FIREBASE_DATABASE_URL = 'https://smart-tourist-b04fd-default-rtdb.asia-southeast1.firebasedatabase.app/'

if not firebase_admin._apps:
    cred = credentials.Certificate(FIREBASE_CREDS_PATH)
    firebase_admin.initialize_app(cred, {'databaseURL': FIREBASE_DATABASE_URL})

db_ref = db.reference()

with open(DATA_FILE, 'r') as f:
    simulation_data = json.load(f)

tourists = simulation_data['tourists']
num_timestamps = simulation_data['metadata']['timestamps']
interval = simulation_data['metadata']['interval_seconds']

speed_mode = sys.argv[1] if len(sys.argv) > 1 else 'realtime'

speed_map = {
    'realtime': interval,
    'fast': 1,
    'instant': 0
}

sleep_time = speed_map.get(speed_mode, interval)

print(f"Starting simulation with {len(tourists)} tourists")
print(f"Mode: {speed_mode} (sleep: {sleep_time}s)")

for t in range(num_timestamps):
    print(f"\nTimestamp {t}/{num_timestamps}")
    
    for tourist in tourists:
        position = tourist['positions'][t]
        
        location_data = {
            'tourist_id': tourist['tourist_id'],
            'latitude': position['lat'],
            'longitude': position['lng'],
            'speed_kmph': position['speed'],
            'timestamp': int(time.time() * 1000),
            'eventType': 'SOS' if position['status'] == 'critical' else 'TRACKING'
        }
        
        db_ref.child('locations').push(location_data)
        
        tourist_ref = db_ref.child('tourists').child(tourist['tourist_id'])
        tourist_ref.update({
            'status': position['status'],
            'current_zone': position['current_zone'],
            'last_location': {
                'lat': position['lat'],
                'lng': position['lng'],
                'timestamp': int(time.time() * 1000)
            }
        })
    
    if sleep_time > 0:
        time.sleep(sleep_time)

print("\nSimulation complete")