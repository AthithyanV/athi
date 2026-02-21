"""AI-powered rice quality prediction.

Uses a trained Random Forest classifier to predict rice quality grade
based on batch attributes such as moisture percentage, weight, and variety.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier


GRADE_MAP = {"A+": 4, "A": 3, "B+": 2, "B": 1, "C": 0}
GRADE_LABELS = ["C", "B", "B+", "A", "A+"]

VARIETY_MAP = {
    "Basmati": 5,
    "Jasmine": 4,
    "Sona Masoori": 3,
    "Ponni": 2,
    "Brown Rice": 1,
    "Wild Rice": 0,
}


def _generate_training_data(n_samples=500):
    """Generate synthetic training data for the quality model."""
    rng = np.random.RandomState(42)
    X = []
    y = []
    for _ in range(n_samples):
        variety_code = rng.randint(0, 6)
        moisture = rng.uniform(8, 20)
        weight = rng.uniform(100, 10000)
        broken_pct = rng.uniform(0, 30)

        # Heuristic labelling: lower moisture + lower broken + higher variety = better
        score = (20 - moisture) * 2 + (30 - broken_pct) * 1.5 + variety_code * 3
        if score > 70:
            grade = 4
        elif score > 55:
            grade = 3
        elif score > 40:
            grade = 2
        elif score > 25:
            grade = 1
        else:
            grade = 0

        X.append([variety_code, moisture, weight, broken_pct])
        y.append(grade)

    return np.array(X), np.array(y)


class QualityPredictor:
    """Predicts rice quality grade from batch attributes."""

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=50, random_state=42, max_depth=8
        )
        self._train()

    def _train(self):
        X, y = _generate_training_data()
        self.model.fit(X, y)

    def predict(self, variety, moisture_pct, weight_kg, broken_pct=5.0):
        """Predict quality grade for a rice batch.

        Returns the predicted grade string and confidence score.
        """
        variety_code = VARIETY_MAP.get(variety, 0)
        features = np.array([[variety_code, moisture_pct, weight_kg, broken_pct]])
        pred = self.model.predict(features)[0]
        proba = self.model.predict_proba(features)[0]
        confidence = float(np.max(proba))
        return GRADE_LABELS[pred], round(confidence, 2)

    def predict_batch(self, batch):
        """Predict quality grade for a RiceBatch object."""
        grade, confidence = self.predict(
            batch.variety, batch.moisture_pct, batch.weight_kg
        )
        batch.predicted_grade = grade
        return grade, confidence
