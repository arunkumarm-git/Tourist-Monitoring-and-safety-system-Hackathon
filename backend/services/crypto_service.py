import hashlib
import hmac
import json
import config

class CryptoService:
    def __init__(self):
        self.secret_key = config.SECRET_KEY
    
    def hash_data(self, data: str) -> str:
        return hashlib.sha256(data.encode()).hexdigest()
    
    def generate_signature(self, data: dict) -> str:
        message = json.dumps(data, sort_keys=True)
        return hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify_signature(self, data: dict, signature: str) -> bool:
        expected = self.generate_signature(data)
        return hmac.compare_digest(expected, signature)