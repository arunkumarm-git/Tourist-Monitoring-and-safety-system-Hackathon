from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import config
from routes import tourists_bp, alerts_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

CORS(app, origins=config.ALLOWED_ORIGINS)
socketio = SocketIO(app, cors_allowed_origins=config.ALLOWED_ORIGINS)

app.register_blueprint(tourists_bp, url_prefix='/api')
app.register_blueprint(alerts_bp, url_prefix='/api')

@app.route('/')
def index():
    return {"service": "T-MASS Backend", "status": "running", "version": "1.0.0"}

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    socketio.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG)
