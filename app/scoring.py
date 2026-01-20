# app/scoring.py

def color_score(base, items):
    base_colors = set(base["colors"])
    score = 0

    for item in items:
        item_colors = set(item["colors"])

        if "neutral" in base_colors or "neutral" in item_colors:
            score += 1.0
        elif base_colors & item_colors:
            score += 0.7
        else:
            score += 0.3

    return round(score / len(items), 2)


def style_score(base, items):
    base_styles = set(base["style"])
    score = 0

    for item in items:
        item_styles = set(item["style"])

        if base_styles & item_styles:
            score += 1.0
        elif base_styles or item_styles:
            score += 0.6
        else:
            score += 0.0

    return round(score / len(items), 2)


def occasion_score(base, items):
    base_occasions = set(base["occasion"])
    score = 0

    for item in items:
        item_occasions = set(item["occasion"])

        if base_occasions & item_occasions:
            score += 1.0
        else:
            score += 0.0

    return round(score / len(items), 2)


def budget_score(base, items):
    base_price = base["price"]

    # If base price is unknown, give neutral score
    if not base_price or base_price <= 0:
        return 0.5

    score = 0

    for item in items:
        item_price = item["price"]

        if not item_price or item_price <= 0:
            score += 0.5
            continue

        diff = abs(item_price - base_price) / base_price

        if diff <= 0.4:
            score += 1.0
        elif diff <= 0.6:
            score += 0.6
        else:
            score += 0.3

    return round(score / len(items), 2)


def final_score(base, items):
    """
    Weighted final score ∈ [0,1]
    """

    c = color_score(base, items)
    s = style_score(base, items)
    o = occasion_score(base, items)
    b = budget_score(base, items)

    final = (
        0.35 * c +
        0.30 * s +
        0.20 * o +
        0.15 * b
    )

    return round(min(final, 1.0), 2)
