"""Slot allocation data model."""

import uuid
from datetime import datetime, timezone


class SlotAllocation:
    """Represents a buyer slot allocation for a rice batch."""

    def __init__(self, batch_id, buyer_id, allocated_kg, variety, quality_grade):
        self.id = str(uuid.uuid4())[:8]
        self.batch_id = batch_id
        self.buyer_id = buyer_id
        self.allocated_kg = float(allocated_kg)
        self.variety = variety
        self.quality_grade = quality_grade
        self.status = "Pending"  # Pending, Confirmed, Delivered
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.score = 0.0  # AI-assigned match score

    def confirm(self):
        self.status = "Confirmed"

    def deliver(self):
        self.status = "Delivered"

    def to_dict(self):
        return {
            "id": self.id,
            "batch_id": self.batch_id,
            "buyer_id": self.buyer_id,
            "allocated_kg": self.allocated_kg,
            "variety": self.variety,
            "quality_grade": self.quality_grade,
            "status": self.status,
            "score": self.score,
            "created_at": self.created_at,
        }
