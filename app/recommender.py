# app/recommender.py
from app.scoring import final_score


def generate_outfits(base, products, max_outfits=3):
    """
    Generate stylist-inspired outfits using deterministic,
    rule-based compatibility and weighted scoring.
    """

    # --------------------------------------------------
    # 1. Base product context
    # --------------------------------------------------
    base_context = {
        "id": base["id"],
        "category": base["category"],
        "gender": base["gender"],
        "colors": base["colors"],
        "style": base["style"],
        "occasion": base["occasion"],
        "price": base["price"],
        "price_bucket": base.get("price_bucket", "unknown"),
    }

    base_is_accessory = base_context["category"] == "accessory"

    outfits = []
    used_ids = {base_context["id"]}

    # --------------------------------------------------
    # 2. Fast candidate filtering
    # --------------------------------------------------
    def fast_candidate_filter(p):
        # Gender
        if not (
            base_context["gender"] == "unisex"
            or p["gender"] == "unisex"
            or p["gender"] == base_context["gender"]
        ):
            return False

        # Occasion
        if not set(base_context["occasion"]) & set(p["occasion"]):
            return False

        # Price range ±40%
        if base_context["price"] > 0 and p["price"] > 0:
            diff = abs(p["price"] - base_context["price"]) / base_context["price"]
            if diff > 0.4:
                return False

        return True

    # --------------------------------------------------
    # 3. Compatibility rules
    # --------------------------------------------------
    def color_compatible(item):
        if "neutral" in base_context["colors"] or "neutral" in item["colors"]:
            return True
        return bool(set(base_context["colors"]) & set(item["colors"]))

    STYLE_COMPATIBILITY = {
        "athleisure": {"athleisure", "casual"},
        "casual": {"casual", "athleisure"},
        "street": {"street"},
        "formal": {"formal"},
    }

    def style_compatible(item):
        for bs in base_context["style"]:
            if any(s in STYLE_COMPATIBILITY.get(bs, set()) for s in item["style"]):
                return True
        return False

    def occasion_compatible(item):
        return bool(set(base_context["occasion"]) & set(item["occasion"]))

    # --------------------------------------------------
    # 4. Candidate pools
    # --------------------------------------------------
    def pool(category):
        return [
            p for p in products
            if p["category"] == category
            and p["id"] not in used_ids
            and fast_candidate_filter(p)
            and color_compatible(p)
            and style_compatible(p)
            and occasion_compatible(p)
        ]

    tops = pool("top")
    bottoms = pool("bottom")
    shoes = pool("footwear")

    accessories = []
    if not base_is_accessory:
        accessories = pool("accessory")

    # --------------------------------------------------
    # 5. Outfit assembly with fallbacks
    # --------------------------------------------------
    i = 0
    while len(outfits) < max_outfits:

        if not tops:
            break

        top = tops[i % len(tops)]
        bottom = bottoms[(i + 1) % len(bottoms)] if bottoms else None
        shoe = shoes[(i + 2) % len(shoes)] if shoes else None

        outfit_items = {}

        # Primary path
        if bottom and shoe:
            outfit_items = {
                "top": top,
                "bottom": bottom,
                "footwear": shoe,
            }

        # Fallback path 1
        elif bottom:
            outfit_items = {
                "top": top,
                "bottom": bottom,
            }

        # Fallback path 2
        elif shoe:
            outfit_items = {
                "top": top,
                "footwear": shoe,
            }

        else:
            i += 1
            continue

        # --------------------------------------------------
        # Guarantee exactly ONE accessory
        # --------------------------------------------------
        if base_is_accessory:
            outfit_items["accessory"] = base
        elif accessories:
            acc = accessories.pop(0)
            outfit_items["accessory"] = acc
            used_ids.add(acc["id"])
        else:
            i += 1
            continue

        # Mark used items
        for item in outfit_items.values():
            used_ids.add(item["id"])

        score = final_score(base, list(outfit_items.values()))

        outfits.append({
            "items": outfit_items,
            "match_score": score,
            "explanation": {
                "color": "Balanced color harmony with neutral support",
                "style": "Consistent styling across items",
                "occasion": "Appropriate for base product usage",
                "budget": "Price range remains balanced",
            }
        })

        i += 1

    return outfits



"""
AI Usage Note:
--------------
This system uses a hybrid AI approach:
- Deterministic rule-based filtering
- Weighted heuristic scoring

No LLMs are used at runtime to guarantee:
- Sub-1s latency
- Predictable behavior
- Cost efficiency

Extensibility:
--------------
An LLM-based reasoning layer (e.g., stylist explanation generation)
can be added asynchronously in the future without affecting
the core recommendation latency.
"""
