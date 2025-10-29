import firebase_admin
from firebase_admin import credentials, db
import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
from services.firebase_service import FirebaseService
from services.supabase_service import SupabaseService

class LocationListener:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(config.FIREBASE_CREDS_PATH)
            firebase_admin.initialize_app(cred, {'databaseURL': config.FIREBASE_DATABASE_URL})
        
        self.firebase_service = FirebaseService()
        self.supabase_service = SupabaseService()
    
    def listener(self, event):
        if event.event_type == 'put' and event.path != '/' and event.data:
            event_data = event.data
            unique_id = event.path.lstrip('/')
            
            if isinstance(event_data, dict) and 'eventType' in event_data:
                if event_data['eventType'] == 'SOS':
                    print(f"SOS EVENT DETECTED: {unique_id}")
                    self.handle_sos(event_data, unique_id)
                elif event_data['eventType'] == 'TRACKING':
                    self.handle_tracking(event_data, unique_id)
    
    def handle_sos(self, event_data, unique_id):
        tourist_id = event_data.get('tourist_id', unique_id)
        lat = event_data.get('latitude')
        lng = event_data.get('longitude')
        
        alert_data = {
            'tourist_id': tourist_id,
            'alert_type': 'sos',
            'alert_level': 3,
            'location_lat': lat,
            'location_lng': lng,
            'zone_type': 'unknown'
        }
        
        alert_id = self.firebase_service.create_alert(alert_data)
        self.supabase_service.insert_alert(alert_id, alert_data)
        self.firebase_service.update_tourist_status(tourist_id, 'critical')
    
    def handle_tracking(self, event_data, unique_id):
        tourist_id = event_data.get('tourist_id', unique_id)
        lat = event_data.get('latitude')
        lng = event_data.get('longitude')
        
        self.firebase_service.update_tourist_status(tourist_id, 'active')
    
    def start(self):
        print("Starting location listener...")
        locations_ref = db.reference('/locations')
        locations_ref.listen(self.listener)
        
        print("Listener active. Press Ctrl+C to exit.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("Stopping listener...")

if __name__ == '__main__':
    listener = LocationListener()
    listener.start()