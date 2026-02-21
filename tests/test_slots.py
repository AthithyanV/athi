"""Tests for AI quality prediction and slot optimization."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from ai.quality_predictor import QualityPredictor, GRADE_LABELS
from ai.slot_optimizer import allocate_slots, auto_allocate
from models.rice_batch import RiceBatch
from models.buyer import Buyer


def test_quality_prediction_returns_valid_grade():
    predictor = QualityPredictor()
    grade, confidence = predictor.predict("Basmati", 11.0, 500)
    assert grade in GRADE_LABELS
    assert 0.0 <= confidence <= 1.0


def test_quality_prediction_batch():
    predictor = QualityPredictor()
    batch = RiceBatch("Jasmine", 1000, 10.0, "Thailand")
    grade, confidence = predictor.predict_batch(batch)
    assert batch.predicted_grade == grade
    assert grade in GRADE_LABELS


def test_slot_allocation_ranking():
    batch = RiceBatch("Basmati", 500, 12.0, "Punjab")
    batch.predicted_grade = "A"

    buyer1 = Buyer("Buyer1", "Co1", ["Basmati"], 1000)
    buyer2 = Buyer("Buyer2", "Co2", ["Jasmine"], 1000)

    results = allocate_slots(batch, [buyer1, buyer2])
    assert len(results) == 2
    # Buyer who prefers Basmati should score higher
    assert results[0][0].name == "Buyer1"
    assert results[0][2] > results[1][2]


def test_auto_allocate():
    batch = RiceBatch("Ponni", 300, 13.0, "Tamil Nadu")
    batch.predicted_grade = "B+"

    buyer = Buyer("TestBuyer", "TestCo", ["Ponni"], 500)
    result = auto_allocate(batch, [buyer])
    assert result is not None
    assert result[0].name == "TestBuyer"
    assert result[1] == 300.0  # Should allocate full batch


def test_auto_allocate_no_capacity():
    batch = RiceBatch("Ponni", 300, 13.0, "Tamil Nadu")
    batch.predicted_grade = "B"

    buyer = Buyer("FullBuyer", "FullCo", ["Ponni"], 100)
    buyer.total_purchased_kg = 100  # Already at max capacity
    result = auto_allocate(batch, [buyer])
    assert result is None


def test_slot_allocation_respects_capacity():
    batch = RiceBatch("Basmati", 500, 12.0, "Punjab")
    batch.predicted_grade = "A"

    buyer = Buyer("PartBuyer", "PartCo", ["Basmati"], 200)
    results = allocate_slots(batch, [buyer])
    assert len(results) == 1
    assert results[0][1] == 200.0  # Can only take 200 of the 500
