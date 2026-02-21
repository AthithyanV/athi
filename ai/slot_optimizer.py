"""AI-powered buyer slot optimization.

Allocates rice batches to buyers using a scoring algorithm that considers
buyer preference, remaining capacity, and quality grade match.
"""


GRADE_VALUE = {"A+": 5, "A": 4, "B+": 3, "B": 2, "C": 1}


def _compute_match_score(buyer, batch_variety, batch_quality, batch_weight):
    """Compute a match score between a buyer and a rice batch.

    Higher score means better match. Considers:
    - Variety preference (does the buyer want this variety?)
    - Quality grade value
    - Remaining capacity fit
    """
    score = 0.0

    # Variety preference bonus
    if batch_variety in buyer.preferred_varieties:
        score += 40.0

    # Quality value bonus
    score += GRADE_VALUE.get(batch_quality, 1) * 5.0

    # Capacity fit: prefer buyers who can take the full batch
    remaining = buyer.max_quantity_kg - buyer.total_purchased_kg
    if remaining >= batch_weight:
        score += 30.0
    elif remaining > 0:
        score += 15.0 * (remaining / batch_weight)

    # Active buyer bonus
    if buyer.active:
        score += 10.0

    return round(score, 2)


def allocate_slots(batch, buyers):
    """Allocate a rice batch to the best-matching buyers.

    Returns a list of (buyer, allocated_kg, score) tuples sorted by score.
    Only returns buyers with positive remaining capacity.
    """
    if not batch.quality_grade and not batch.predicted_grade:
        return []

    quality = batch.quality_grade or batch.predicted_grade
    candidates = []

    for buyer in buyers:
        if not buyer.active:
            continue
        remaining = buyer.max_quantity_kg - buyer.total_purchased_kg
        if remaining <= 0:
            continue

        score = _compute_match_score(
            buyer, batch.variety, quality, batch.weight_kg
        )
        alloc_kg = min(batch.weight_kg, remaining)
        candidates.append((buyer, alloc_kg, score))

    # Sort by score descending
    candidates.sort(key=lambda x: x[2], reverse=True)
    return candidates


def auto_allocate(batch, buyers):
    """Automatically allocate a batch to the single best buyer.

    Returns (buyer, allocated_kg, score) or None if no suitable buyer.
    """
    candidates = allocate_slots(batch, buyers)
    if candidates:
        return candidates[0]
    return None
