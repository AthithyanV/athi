"""Rice batch data model."""

import uuid
from datetime import datetime, timezone


class RiceBatch:
    """Represents a batch of rice being processed."""

    STAGES = [
        "Intake",
        "Cleaning",
        "Dehusking",
        "Milling",
        "Polishing",
        "Grading",
        "Packaging",
    ]

    def __init__(self, variety, weight_kg, moisture_pct, origin):
        self.id = str(uuid.uuid4())[:8]
        self.variety = variety
        self.weight_kg = float(weight_kg)
        self.moisture_pct = float(moisture_pct)
        self.origin = origin
        self.current_stage = "Intake"
        self.quality_grade = None
        self.predicted_grade = None
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = self.created_at
        self.processing_notes = []

    def advance_stage(self):
        """Move the batch to the next processing stage.

        Returns True if advanced, False if already at last stage.
        """
        idx = self.STAGES.index(self.current_stage)
        if idx < len(self.STAGES) - 1:
            self.current_stage = self.STAGES[idx + 1]
            self.updated_at = datetime.now(timezone.utc).isoformat()
            return True
        return False

    def set_quality_grade(self, grade):
        """Assign a quality grade to this batch."""
        self.quality_grade = grade
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "variety": self.variety,
            "weight_kg": self.weight_kg,
            "moisture_pct": self.moisture_pct,
            "origin": self.origin,
            "current_stage": self.current_stage,
            "quality_grade": self.quality_grade,
            "predicted_grade": self.predicted_grade,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "processing_notes": self.processing_notes,
        }
