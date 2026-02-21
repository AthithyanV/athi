# 🌾 AI-Powered Rice Processing & Buyer Slot Allocation

A full-stack web application for managing rice processing operations with **AI-powered quality prediction**, **smart buyer slot allocation**, and a **real-time dashboard**.

## Features

- **Rice Batch Management** – Create and track rice batches through 7 processing stages (Intake → Cleaning → Dehusking → Milling → Polishing → Grading → Packaging)
- **AI Quality Prediction** – Machine learning model (Random Forest) predicts rice quality grade (A+, A, B+, B, C) based on variety, moisture, and weight
- **Smart Buyer Slot Allocation** – AI-optimized matching algorithm scores and allocates batches to buyers based on variety preference, quality grade, and capacity
- **Real-Time Dashboard** – Live-updating dashboard with WebSocket support showing processing stats, quality distribution charts, and allocation status
- **RESTful API** – Complete JSON API for programmatic access

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | Python, Flask, Flask-SocketIO |
| AI/ML | scikit-learn (Random Forest), NumPy |
| Real-time | WebSockets (Socket.IO) |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Testing | pytest |

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Open http://localhost:5000 in your browser
```

## API Endpoints

### Rice Batches
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/batches` | List all batches |
| POST | `/api/batches` | Create a new batch (triggers AI prediction) |
| GET | `/api/batches/<id>` | Get batch details |
| POST | `/api/batches/<id>/advance` | Advance to next processing stage |

### Buyers
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/buyers` | List all buyers |
| POST | `/api/buyers` | Register a new buyer |
| GET | `/api/buyers/<id>` | Get buyer details |

### Slot Allocation
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/slots` | List all allocations |
| GET | `/api/slots/recommend/<batch_id>` | Get AI-ranked buyer recommendations |
| POST | `/api/slots/auto-allocate/<batch_id>` | Auto-allocate batch to best buyer |
| POST | `/api/slots/<id>/confirm` | Confirm an allocation |
| POST | `/api/slots/<id>/deliver` | Mark allocation as delivered |

### Dashboard
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats` | Get aggregated dashboard statistics |

## Project Structure

```
├── app.py                    # Flask application factory
├── config.py                 # Configuration settings
├── requirements.txt          # Python dependencies
├── ai/
│   ├── quality_predictor.py  # ML-based quality grade prediction
│   └── slot_optimizer.py     # AI buyer-batch matching algorithm
├── models/
│   ├── rice_batch.py         # Rice batch data model
│   ├── buyer.py              # Buyer data model
│   └── slot.py               # Slot allocation data model
├── routes/
│   ├── processing.py         # Batch processing API routes
│   ├── buyers.py             # Buyer management API routes
│   ├── slots.py              # Slot allocation API routes
│   └── dashboard.py          # Dashboard statistics API routes
├── templates/
│   └── dashboard.html        # Real-time dashboard UI
├── static/
│   ├── css/dashboard.css     # Dashboard styles
│   └── js/dashboard.js       # Dashboard real-time logic
└── tests/
    ├── test_processing.py    # Batch model tests
    ├── test_buyers.py        # Buyer model tests
    ├── test_slots.py         # AI prediction & allocation tests
    └── test_api.py           # API endpoint tests
```

## Running Tests

```bash
python -m pytest tests/ -v
```