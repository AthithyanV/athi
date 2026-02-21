"""Buyer management API routes."""

from flask import Blueprint, request, jsonify


def init_buyer_routes(store, socketio):
    """Create and return buyer blueprint with shared state."""
    bp = Blueprint("buyers", __name__)

    @bp.route("/api/buyers", methods=["GET"])
    def list_buyers():
        return jsonify([b.to_dict() for b in store["buyers"]])

    @bp.route("/api/buyers", methods=["POST"])
    def create_buyer():
        from models.buyer import Buyer

        data = request.get_json()
        required = ["name", "company", "preferred_varieties", "max_quantity_kg"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        buyer = Buyer(
            name=data["name"],
            company=data["company"],
            preferred_varieties=data["preferred_varieties"],
            max_quantity_kg=data["max_quantity_kg"],
        )
        store["buyers"].append(buyer)
        socketio.emit("buyer_update", {"buyers": [b.to_dict() for b in store["buyers"]]})
        return jsonify(buyer.to_dict()), 201

    @bp.route("/api/buyers/<buyer_id>", methods=["GET"])
    def get_buyer(buyer_id):
        buyer = next((b for b in store["buyers"] if b.id == buyer_id), None)
        if not buyer:
            return jsonify({"error": "Buyer not found"}), 404
        return jsonify(buyer.to_dict())

    return bp
