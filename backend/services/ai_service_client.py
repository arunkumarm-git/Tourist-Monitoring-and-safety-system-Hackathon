import requests
import config

class AIServiceClient:
    def __init__(self):
        self.base_url = config.AI_SERVICE_URL
    
    def analyze_tourists(self, tourists_data):
        url = f"{self.base_url}/analyze"
        response = requests.post(url, json={'tourists': tourists_data}, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def cluster_only(self, tourists_data):
        url = f"{self.base_url}/cluster"
        response = requests.post(url, json={'tourists': tourists_data}, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def get_zones(self):
        url = f"{self.base_url}/zones"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_config(self):
        url = f"{self.base_url}/config"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()