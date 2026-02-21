"""Tests for buyer management."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.buyer import Buyer


def test_create_buyer():
    buyer = Buyer("Ravi", "RiceCo", ["Basmati", "Jasmine"], 5000)
    assert buyer.name == "Ravi"
    assert buyer.company == "RiceCo"
    assert buyer.max_quantity_kg == 5000.0
    assert buyer.active is True


def test_buyer_to_dict():
    buyer = Buyer("Meena", "GrainMart", ["Ponni"], 3000)
    d = buyer.to_dict()
    assert d["name"] == "Meena"
    assert d["remaining_capacity_kg"] == 3000.0
    assert d["preferred_varieties"] == ["Ponni"]
