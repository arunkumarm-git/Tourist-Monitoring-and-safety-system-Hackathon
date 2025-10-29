import firebase_admin
from firebase_admin import credentials, db
import config
import uuid
from datetime import datetime

class FirebaseService:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(config.FIREBASE_CREDS_PATH)
            firebase_admin.initialize_app(cred, {'databaseURL': config.FIREBASE_DATABASE_URL})
        
        self.db = db.reference()
    
    def get_server_timestamp(self):
        return int(datetime.utcnow().timestamp() * 1000)
    
    def get_all_tourists(self):
        tourists_ref = self.db.child('tourists')
        return tourists_ref.get() or {}
    
    def get_tourist(self, tourist_id):
        tourist_ref = self.db.child('tourists').child(tourist_id)
        return tourist_ref.get()
    
    def set_tourist_status(self, tourist_id, data):
        tourist_ref = self.db.child('tourists').child(tourist_id)
        tourist_ref.set(data)
    
    def update_tourist_status(self, tourist_id, status):
        tourist_ref = self.db.child('tourists').child(tourist_id)
        tourist_ref.update({'status': status, 'last_update': self.get_server_timestamp()})
    
    def create_alert(self, alert_data):
        alert_id = str(uuid.uuid4())
        alert_ref = self.db.child('alerts').child(alert_id)
        alert_data['timestamp'] = self.get_server_timestamp()
        alert_data['resolved'] = False
        alert_ref.set(alert_data)
        return alert_id
    
    def get_all_alerts(self):
        alerts_ref = self.db.child('alerts')
        return alerts_ref.get() or {}
    
    def get_alert(self, alert_id):
        alert_ref = self.db.child('alerts').child(alert_id)
        return alert_ref.get()
    
    def resolve_alert(self, alert_id):
        alert_ref = self.db.child('alerts').child(alert_id)
        alert_ref.update({
            'resolved': True,
            'resolution_timestamp': self.get_server_timestamp()
        })
    
    def get_zones(self):
        zones_ref = self.db.child('zones')
        return zones_ref.get() or {}
    
    def get_clusters(self, timestamp):
        clusters_ref = self.db.child('clusters').child(str(timestamp))
        return clusters_ref.get()
    
    def store_clusters(self, timestamp, clusters_data):
        clusters_ref = self.db.child('clusters').child(str(timestamp))
        clusters_ref.set(clusters_data)
    
    def get_all_locations(self):
        locations_ref = self.db.child('locations')
        return locations_ref.get() or {}