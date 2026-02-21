"""Tests for rice batch processing."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from models.rice_batch import RiceBatch


def test_create_batch():
    batch = RiceBatch("Basmati", 500, 12.5, "Punjab")
    assert batch.variety == "Basmati"
    assert batch.weight_kg == 500.0
    assert batch.moisture_pct == 12.5
    assert batch.origin == "Punjab"
    assert batch.current_stage == "Intake"
    assert batch.quality_grade is None


def test_advance_stage():
    batch = RiceBatch("Jasmine", 300, 11.0, "Thailand")
    assert batch.current_stage == "Intake"
    assert batch.advance_stage() is True
    assert batch.current_stage == "Cleaning"
    assert batch.advance_stage() is True
    assert batch.current_stage == "Dehusking"


def test_advance_to_final_stage():
    batch = RiceBatch("Ponni", 200, 13.0, "Tamil Nadu")
    for _ in range(6):
        assert batch.advance_stage() is True
    assert batch.current_stage == "Packaging"
    assert batch.advance_stage() is False  # Already at last stage


def test_set_quality_grade():
    batch = RiceBatch("Basmati", 1000, 10.0, "Haryana")
    batch.set_quality_grade("A+")
    assert batch.quality_grade == "A+"


def test_to_dict():
    batch = RiceBatch("Sona Masoori", 750, 14.0, "Andhra Pradesh")
    d = batch.to_dict()
    assert d["variety"] == "Sona Masoori"
    assert d["weight_kg"] == 750.0
    assert "id" in d
    assert "created_at" in d
