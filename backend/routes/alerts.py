from flask import Blueprint, request, jsonify
from services.firebase_service import FirebaseService
from services.supabase_service import SupabaseService

alerts_bp = Blueprint('alerts', __name__)

firebase_service = FirebaseService()
supabase_service = SupabaseService()

@alerts_bp.route('/alerts', methods=['GET'])
def get_all_alerts():
    try:
        alerts = firebase_service.get_all_alerts()
        return jsonify(alerts), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@alerts_bp.route('/alerts/<alert_id>', methods=['GET'])
def get_alert(alert_id):
    try:
        alert = firebase_service.get_alert(alert_id)
        if not alert:
            return jsonify({'error': 'Alert not found'}), 404
        return jsonify(alert), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@alerts_bp.route('/alerts/<alert_id>/resolve', methods=['POST'])
def resolve_alert(alert_id):
    try:
        firebase_service.resolve_alert(alert_id)
        supabase_service.resolve_alert(alert_id)
        return jsonify({'status': 'resolved'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@alerts_bp.route('/zones', methods=['GET'])
def get_zones():
    try:
        zones = firebase_service.get_zones()
        return jsonify(zones), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@alerts_bp.route('/clusters/<int:timestamp>', methods=['GET'])
def get_clusters(timestamp):
    try:
        clusters = firebase_service.get_clusters(timestamp)
        return jsonify(clusters), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500