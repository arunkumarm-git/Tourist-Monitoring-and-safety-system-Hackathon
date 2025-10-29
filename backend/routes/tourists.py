from flask import Blueprint, request, jsonify
from services.firebase_service import FirebaseService
from services.supabase_service import SupabaseService
from services.crypto_service import CryptoService
import uuid

tourists_bp = Blueprint('tourists', __name__)

firebase_service = FirebaseService()
supabase_service = SupabaseService()
crypto_service = CryptoService()

@tourists_bp.route('/register', methods=['POST'])
def register_tourist():
    try:
        data = request.json
        
        tourist_id = str(uuid.uuid4())
        
        name_hash = crypto_service.hash_data(data['name'])
        passport_hash = crypto_service.hash_data(data['passport_number'])
        phone_hash = crypto_service.hash_data(data['phone'])
        
        tourist_data = {
            'id': tourist_id,
            'name_hash': name_hash,
            'passport_hash': passport_hash,
            'phone_hash': phone_hash,
            'nationality': data['nationality'],
        }
        
        signature = crypto_service.generate_signature(tourist_data)
        tourist_data['audit_signature'] = signature
        
        supabase_service.insert_tourist(tourist_data)
        
        firebase_service.set_tourist_status(tourist_id, {
            'status': 'active',
            'current_zone': 'safe',
            'last_update': firebase_service.get_server_timestamp()
        })
        
        return jsonify({'tourist_id': tourist_id, 'status': 'registered'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tourists_bp.route('/tourists', methods=['GET'])
def get_all_tourists():
    try:
        tourists = firebase_service.get_all_tourists()
        return jsonify(tourists), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tourists_bp.route('/tourists/<tourist_id>', methods=['GET'])
def get_tourist(tourist_id):
    try:
        tourist = firebase_service.get_tourist(tourist_id)
        if not tourist:
            return jsonify({'error': 'Tourist not found'}), 404
        return jsonify(tourist), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@tourists_bp.route('/sos', methods=['POST'])
def handle_sos():
    try:
        data = request.json
        tourist_id = data.get('tourist_id')
        lat = data.get('latitude')
        lng = data.get('longitude')
        
        alert_data = {
            'tourist_id': tourist_id,
            'alert_type': 'sos',
            'alert_level': 3,
            'location_lat': lat,
            'location_lng': lng,
            'zone_type': 'unknown'
        }
        
        alert_id = firebase_service.create_alert(alert_data)
        
        supabase_service.insert_alert(alert_id, alert_data)
        
        firebase_service.update_tourist_status(tourist_id, 'critical')
        
        return jsonify({'alert_id': alert_id, 'status': 'sos_received'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500