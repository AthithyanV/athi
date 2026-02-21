"""Rice processing API routes."""

from flask import Blueprint, request, jsonify


def init_processing_routes(store, quality_predictor, socketio):
    """Create and return processing blueprint with shared state."""
    bp = Blueprint("processing", __name__)

    @bp.route("/api/batches", methods=["GET"])
    def list_batches():
        return jsonify([b.to_dict() for b in store["batches"]])

    @bp.route("/api/batches", methods=["POST"])
    def create_batch():
        from models.rice_batch import RiceBatch

        data = request.get_json()
        required = ["variety", "weight_kg", "moisture_pct", "origin"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        batch = RiceBatch(
            variety=data["variety"],
            weight_kg=data["weight_kg"],
            moisture_pct=data["moisture_pct"],
            origin=data["origin"],
        )

        # AI quality prediction
        grade, confidence = quality_predictor.predict_batch(batch)
        batch.processing_notes.append(
            f"AI predicted grade: {grade} (confidence: {confidence})"
        )

        store["batches"].append(batch)
        socketio.emit("batch_update", {"batches": [b.to_dict() for b in store["batches"]]})
        return jsonify(batch.to_dict()), 201

    @bp.route("/api/batches/<batch_id>", methods=["GET"])
    def get_batch(batch_id):
        batch = next((b for b in store["batches"] if b.id == batch_id), None)
        if not batch:
            return jsonify({"error": "Batch not found"}), 404
        return jsonify(batch.to_dict())

    @bp.route("/api/batches/<batch_id>/advance", methods=["POST"])
    def advance_batch(batch_id):
        batch = next((b for b in store["batches"] if b.id == batch_id), None)
        if not batch:
            return jsonify({"error": "Batch not found"}), 404

        if batch.advance_stage():
            # When reaching Grading stage, finalize grade from AI prediction
            if batch.current_stage == "Grading" and batch.predicted_grade:
                batch.set_quality_grade(batch.predicted_grade)
                batch.processing_notes.append(
                    f"Quality grade finalized: {batch.quality_grade}"
                )
            socketio.emit("batch_update", {"batches": [b.to_dict() for b in store["batches"]]})
            return jsonify(batch.to_dict())

        return jsonify({"error": "Batch already at final stage"}), 400

    return bp
