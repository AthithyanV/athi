"""AI-Powered Rice Processing & Buyer Slot Allocation System.

Main application entry point with Flask and SocketIO for real-time updates.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_cors import CORS

from config import Config
from ai.quality_predictor import QualityPredictor
from routes.processing import init_processing_routes
from routes.buyers import init_buyer_routes
from routes.slots import init_slot_routes
from routes.dashboard import init_dashboard_routes


def create_app():
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    socketio = SocketIO(app, cors_allowed_origins="*")

    # Per-app in-memory data store
    store = {
        "batches": [],
        "buyers": [],
        "slots": [],
    }

    # Initialize AI models
    quality_predictor = QualityPredictor()

    # Register blueprints
    app.register_blueprint(init_processing_routes(store, quality_predictor, socketio))
    app.register_blueprint(init_buyer_routes(store, socketio))
    app.register_blueprint(init_slot_routes(store, socketio))
    app.register_blueprint(init_dashboard_routes(store))

    @app.route("/")
    def index():
        return render_template("dashboard.html")

    @socketio.on("connect")
    def handle_connect():
        socketio.emit("batch_update", {"batches": [b.to_dict() for b in store["batches"]]})
        socketio.emit("buyer_update", {"buyers": [b.to_dict() for b in store["buyers"]]})
        socketio.emit("slot_update", {"slots": [s.to_dict() for s in store["slots"]]})

    return app, socketio


if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
