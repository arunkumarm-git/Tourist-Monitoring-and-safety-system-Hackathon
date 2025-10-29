from supabase import create_client, Client
import config
from datetime import datetime

class SupabaseService:
    def __init__(self):
        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    
    def insert_tourist(self, tourist_data):
        response = self.client.table('tourists').insert({
            'id': tourist_data['id'],
            'name_hash': tourist_data['name_hash'],
            'passport_hash': tourist_data['passport_hash'],
            'phone_hash': tourist_data['phone_hash'],
            'nationality': tourist_data['nationality'],
            'audit_signature': tourist_data['audit_signature']
        }).execute()
        return response.data
    
    def get_tourist(self, tourist_id):
        response = self.client.table('tourists').select('*').eq('id', tourist_id).execute()
        return response.data[0] if response.data else None
    
    def insert_alert(self, alert_id, alert_data):
        from services.crypto_service import CryptoService
        crypto = CryptoService()
        
        alert_hash = crypto.hash_data(str(alert_data))
        signature = crypto.generate_signature(alert_data)
        
        response = self.client.table('alerts').insert({
            'id': alert_id,
            'tourist_id': alert_data['tourist_id'],
            'alert_type': alert_data['alert_type'],
            'alert_level': alert_data['alert_level'],
            'timestamp': datetime.utcnow().isoformat(),
            'location_lat': alert_data['location_lat'],
            'location_lng': alert_data['location_lng'],
            'zone_type': alert_data.get('zone_type', 'unknown'),
            'audit_hash': alert_hash,
            'signature': signature,
            'resolved': False
        }).execute()
        return response.data
    
    def resolve_alert(self, alert_id):
        response = self.client.table('alerts').update({
            'resolved': True,
            'resolution_timestamp': datetime.utcnow().isoformat()
        }).eq('id', alert_id).execute()
        return response.data
    
    def get_alert(self, alert_id):
        response = self.client.table('alerts').select('*').eq('id', alert_id).execute()
        return response.data[0] if response.data else None
    
    def insert_audit_trail(self, event_type, entity_id, data_hash, previous_hash, signature):
        response = self.client.table('audit_trail').insert({
            'event_type': event_type,
            'entity_id': entity_id,
            'data_hash': data_hash,
            'previous_hash': previous_hash,
            'signature': signature
        }).execute()
        return response.data