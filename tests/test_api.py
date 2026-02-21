"""Tests for Flask API endpoints."""

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


def get_client():
    app, socketio = create_app()
    app.config["TESTING"] = True
    return app.test_client()


def test_dashboard_page():
    client = get_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Rice Processing" in resp.data


def test_create_and_list_batches():
    client = get_client()
    resp = client.post(
        "/api/batches",
        data=json.dumps({
            "variety": "Basmati",
            "weight_kg": 500,
            "moisture_pct": 12.0,
            "origin": "Punjab",
        }),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.get_json()
    assert data["variety"] == "Basmati"
    assert data["predicted_grade"] is not None

    resp = client.get("/api/batches")
    assert resp.status_code == 200
    assert len(resp.get_json()) == 1


def test_create_batch_missing_field():
    client = get_client()
    resp = client.post(
        "/api/batches",
        data=json.dumps({"variety": "Basmati"}),
        content_type="application/json",
    )
    assert resp.status_code == 400


def test_advance_batch():
    client = get_client()
    resp = client.post(
        "/api/batches",
        data=json.dumps({
            "variety": "Jasmine",
            "weight_kg": 300,
            "moisture_pct": 11.0,
            "origin": "Thailand",
        }),
        content_type="application/json",
    )
    batch_id = resp.get_json()["id"]

    resp = client.post(f"/api/batches/{batch_id}/advance")
    assert resp.status_code == 200
    assert resp.get_json()["current_stage"] == "Cleaning"


def test_create_and_list_buyers():
    client = get_client()
    resp = client.post(
        "/api/buyers",
        data=json.dumps({
            "name": "Ravi",
            "company": "RiceCo",
            "preferred_varieties": ["Basmati"],
            "max_quantity_kg": 5000,
        }),
        content_type="application/json",
    )
    assert resp.status_code == 201
    assert resp.get_json()["name"] == "Ravi"

    resp = client.get("/api/buyers")
    assert resp.status_code == 200


def test_dashboard_stats():
    client = get_client()
    resp = client.get("/api/dashboard/stats")
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total_batches" in data
    assert "stage_distribution" in data
