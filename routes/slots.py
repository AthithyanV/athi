"""Slot allocation API routes."""

from flask import Blueprint, request, jsonify
from ai.slot_optimizer import allocate_slots, auto_allocate
from models.slot import SlotAllocation


def init_slot_routes(store, socketio):
    """Create and return slot allocation blueprint with shared state."""
    bp = Blueprint("slots", __name__)

    @bp.route("/api/slots", methods=["GET"])
    def list_slots():
        return jsonify([s.to_dict() for s in store["slots"]])

    @bp.route("/api/slots/recommend/<batch_id>", methods=["GET"])
    def recommend_slots(batch_id):
        batch = next((b for b in store["batches"] if b.id == batch_id), None)
        if not batch:
            return jsonify({"error": "Batch not found"}), 404

        candidates = allocate_slots(batch, store["buyers"])
        results = [
            {
                "buyer": buyer.to_dict(),
                "allocated_kg": alloc_kg,
                "score": score,
            }
            for buyer, alloc_kg, score in candidates
        ]
        return jsonify(results)

    @bp.route("/api/slots/auto-allocate/<batch_id>", methods=["POST"])
    def auto_allocate_batch(batch_id):
        batch = next((b for b in store["batches"] if b.id == batch_id), None)
        if not batch:
            return jsonify({"error": "Batch not found"}), 404

        result = auto_allocate(batch, store["buyers"])
        if not result:
            return jsonify({"error": "No suitable buyer found"}), 404

        buyer, alloc_kg, score = result
        slot = SlotAllocation(
            batch_id=batch.id,
            buyer_id=buyer.id,
            allocated_kg=alloc_kg,
            variety=batch.variety,
            quality_grade=batch.quality_grade or batch.predicted_grade,
        )
        slot.score = score
        buyer.total_purchased_kg += alloc_kg

        store["slots"].append(slot)
        socketio.emit("slot_update", {"slots": [s.to_dict() for s in store["slots"]]})
        socketio.emit("buyer_update", {"buyers": [b.to_dict() for b in store["buyers"]]})
        return jsonify(slot.to_dict()), 201

    @bp.route("/api/slots/<slot_id>/confirm", methods=["POST"])
    def confirm_slot(slot_id):
        slot = next((s for s in store["slots"] if s.id == slot_id), None)
        if not slot:
            return jsonify({"error": "Slot not found"}), 404
        slot.confirm()
        socketio.emit("slot_update", {"slots": [s.to_dict() for s in store["slots"]]})
        return jsonify(slot.to_dict())

    @bp.route("/api/slots/<slot_id>/deliver", methods=["POST"])
    def deliver_slot(slot_id):
        slot = next((s for s in store["slots"] if s.id == slot_id), None)
        if not slot:
            return jsonify({"error": "Slot not found"}), 404
        slot.deliver()
        socketio.emit("slot_update", {"slots": [s.to_dict() for s in store["slots"]]})
        return jsonify(slot.to_dict())

    return bp
