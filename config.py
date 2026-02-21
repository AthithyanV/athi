"""Application configuration."""

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    HOST = os.environ.get("HOST", "0.0.0.0")
    PORT = int(os.environ.get("PORT", 5000))

    # Rice processing configuration
    RICE_VARIETIES = [
        "Basmati",
        "Jasmine",
        "Sona Masoori",
        "Ponni",
        "Brown Rice",
        "Wild Rice",
    ]
    PROCESSING_STAGES = [
        "Intake",
        "Cleaning",
        "Dehusking",
        "Milling",
        "Polishing",
        "Grading",
        "Packaging",
    ]
    QUALITY_GRADES = ["A+", "A", "B+", "B", "C"]
