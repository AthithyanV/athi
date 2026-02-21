"""Buyer data model."""

import uuid
from datetime import datetime, timezone


class Buyer:
    """Represents a rice buyer."""

    def __init__(self, name, company, preferred_varieties, max_quantity_kg):
        self.id = str(uuid.uuid4())[:8]
        self.name = name
        self.company = company
        self.preferred_varieties = preferred_varieties
        self.max_quantity_kg = float(max_quantity_kg)
        self.total_purchased_kg = 0.0
        self.active = True
        self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "company": self.company,
            "preferred_varieties": self.preferred_varieties,
            "max_quantity_kg": self.max_quantity_kg,
            "total_purchased_kg": self.total_purchased_kg,
            "remaining_capacity_kg": self.max_quantity_kg - self.total_purchased_kg,
            "active": self.active,
            "created_at": self.created_at,
        }
