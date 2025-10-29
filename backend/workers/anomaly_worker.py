import time
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
import config
from services.firebase_service import FirebaseService
from services.supabase_service import SupabaseService
from services.ai_service_client import AIServiceClient

class AnomalyWorker:
    def __init__(self):
        self.firebase_service = FirebaseService()
        self.supabase_service = SupabaseService()
        self.ai_client = AIServiceClient()
        self.check_interval = config.ANOMALY_CHECK_INTERVAL
    
    def process_locations(self):
        locations = self.firebase_service.get_all_locations()
        
        if not locations:
            return
        
        tourists_data = []
        for loc_id, loc_data in locations.items():
            if isinstance(loc_data, dict):
                tourists_data.append({
                    'id': loc_data.get('tourist_id', loc_id),
                    'lat': loc_data.get('latitude'),
                    'lng': loc_data.get('longitude'),
                    'speed_kmh': loc_data.get('speed_kmph', 0),
                    'status': 'active'
                })
        
        if not tourists_data:
            return
        
        analysis_result = self.ai_client.analyze_tourists(tourists_data)
        
        timestamp = int(time.time())
        self.firebase_service.store_clusters(timestamp, {
            'clusters': analysis_result['clusters'],
            'stats': analysis_result['stats']
        })
        
        self.evaluate_anomalies(analysis_result)
    
    def evaluate_anomalies(self, analysis_result):
        for tourist in analysis_result['tourists']:
            tourist_id = tourist['id']
            is_outlier = tourist.get('is_outlier', False)
            in_danger = tourist.get('in_danger', False)
            in_restricted = tourist.get('in_restricted', False)
            
            alert_level = 0
            alert_type = 'normal'
            
            if in_danger and is_outlier:
                alert_level = 3
                alert_type = 'critical_danger_zone'
            elif in_danger:
                alert_level = 2
                alert_type = 'danger_zone'
            elif in_restricted and is_outlier:
                alert_level = 2
                alert_type = 'restricted_isolated'
            elif is_outlier:
                alert_level = 1
                alert_type = 'isolation'
            
            if alert_level >= 2:
                alert_data = {
                    'tourist_id': tourist_id,
                    'alert_type': alert_type,
                    'alert_level': alert_level,
                    'location_lat': tourist['lat'],
                    'location_lng': tourist['lng'],
                    'zone_type': tourist.get('zone_type', 'unknown')
                }
                
                alert_id = self.firebase_service.create_alert(alert_data)
                self.supabase_service.insert_alert(alert_id, alert_data)
                
                status = 'critical' if alert_level == 3 else 'warning'
                self.firebase_service.update_tourist_status(tourist_id, status)
    
    def start(self):
        print(f"Starting anomaly detection worker (interval: {self.check_interval}s)...")
        try:
            while True:
                self.process_locations()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            print("Stopping anomaly worker...")

if __name__ == '__main__':
    worker = AnomalyWorker()
    worker.start()