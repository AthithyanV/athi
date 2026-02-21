"""Dashboard API routes."""

from flask import Blueprint, jsonify


def init_dashboard_routes(store):
    """Create and return dashboard blueprint with shared state."""
    bp = Blueprint("dashboard", __name__)

    @bp.route("/api/dashboard/stats", methods=["GET"])
    def dashboard_stats():
        batches = store["batches"]
        buyers = store["buyers"]
        slots = store["slots"]

        # Processing stage distribution
        stage_counts = {}
        for b in batches:
            stage_counts[b.current_stage] = stage_counts.get(b.current_stage, 0) + 1

        # Quality grade distribution
        grade_counts = {}
        for b in batches:
            grade = b.quality_grade or b.predicted_grade or "Pending"
            grade_counts[grade] = grade_counts.get(grade, 0) + 1

        # Variety distribution
        variety_counts = {}
        for b in batches:
            variety_counts[b.variety] = variety_counts.get(b.variety, 0) + 1

        # Allocation stats
        total_allocated = sum(s.allocated_kg for s in slots)
        total_weight = sum(b.weight_kg for b in batches)
        pending_slots = sum(1 for s in slots if s.status == "Pending")
        confirmed_slots = sum(1 for s in slots if s.status == "Confirmed")
        delivered_slots = sum(1 for s in slots if s.status == "Delivered")

        return jsonify({
            "total_batches": len(batches),
            "total_buyers": len(buyers),
            "total_slots": len(slots),
            "total_weight_kg": total_weight,
            "total_allocated_kg": total_allocated,
            "allocation_pct": round(
                (total_allocated / total_weight * 100) if total_weight > 0 else 0, 1
            ),
            "stage_distribution": stage_counts,
            "grade_distribution": grade_counts,
            "variety_distribution": variety_counts,
            "slot_status": {
                "pending": pending_slots,
                "confirmed": confirmed_slots,
                "delivered": delivered_slots,
            },
        })

    return bp
