# app/data_loader.py
import pandas as pd

# -----------------------------
# Controlled keyword dictionaries
# -----------------------------

COLOR_KEYWORDS = {
    "black": ["black", "jet", "ebony"],
    "white": ["white", "cream", "ivory"],
    "red": ["red", "maroon", "burgundy"],
    "blue": ["blue", "navy"],
    "green": ["green", "olive"],
    "pink": ["pink", "rose"],
    "brown": ["brown", "tan", "beige"],
    "grey": ["grey", "gray", "charcoal"],
    "silver": ["silver"],
    "gold": ["gold"],
}

STYLE_KEYWORDS = {
    "athleisure": ["gym", "training", "workout", "active", "sport", "legging"],
    "casual": ["t-shirt", "tee", "hoodie", "jeans", "casual", "daily"],
    "street": ["street", "cargo", "oversized", "urban"],
    "formal": ["formal", "office", "blazer", "shirt"],
}

OCCASION_KEYWORDS = {
    "workout": ["gym", "training", "fitness"],
    "formal": ["formal", "office", "business"],
    "casual": ["casual", "daily", "everyday"],
}

SEASON_KEYWORDS = {
    "winter": ["winter", "jacket", "hoodie", "sweat"],
    "summer": ["summer", "shorts", "tank"],
}

# -----------------------------
# Helper functions
# -----------------------------

def infer_colors(text: str):
    text = text.lower()
    colors = set()
    for color, keywords in COLOR_KEYWORDS.items():
        if any(k in text for k in keywords):
            colors.add(color)
    return list(colors) if colors else ["neutral"]


def infer_from_text(text: str, keyword_map: dict, default="casual"):
    text = text.lower()
    values = set()
    for key, keywords in keyword_map.items():
        if any(k in text for k in keywords):
            values.add(key)
    return list(values) if values else [default]


def infer_season(text: str):
    text = text.lower()
    for season, keywords in SEASON_KEYWORDS.items():
        if any(k in text for k in keywords):
            return [season]
    return ["all"]


def normalize_gender(raw_gender):
    gender = str(raw_gender).lower()
    if gender in ["men", "male"]:
        return "men"
    if gender in ["women", "female"]:
        return "women"
    return "unisex"


def normalize_category(category, sub_category, product_type, title):
    text = f"{category} {sub_category} {product_type} {title}".lower()

    # Accessories FIRST
    if any(k in text for k in ["watch", "belt", "cap", "bottle", "bag", "wallet"]):
        return "accessory"

    if any(k in text for k in ["shoe", "sneaker", "footwear"]):
        return "footwear"

    if any(k in text for k in ["pant", "trouser", "legging", "jean"]):
        return "bottom"

    return "top"


def price_bucket(price: float):
    if price <= 0:
        return "unknown"
    if price < 3000:
        return "low"
    if price < 10000:
        return "mid"
    return "high"

# -----------------------------
# Main loader
# -----------------------------

def load_products(path="data/products.xlsx"):
    df = pd.read_excel(path)
    products = []

    for _, row in df.iterrows():
        text_blob = f"{row['title']} {row['description']} {row['tags']}"

        price = float(row["lowest_price"]) if not pd.isna(row["lowest_price"]) else 0.0

        product = {
            "id": str(row["sku_id"]),
            "name": str(row["title"]),

            "category": normalize_category(
                row["category"],
                row["sub_category"],
                row["product_type"],
                row["title"]
            ),

            "gender": normalize_gender(row["gender"]),

            "colors": infer_colors(text_blob),
            "style": infer_from_text(text_blob, STYLE_KEYWORDS, default="casual"),
            "occasion": infer_from_text(text_blob, OCCASION_KEYWORDS, default="casual"),
            "season": infer_season(text_blob),

            "price": price,
            "price_bucket": price_bucket(price),

            "brand": str(row["brand_name"]),
            "image": row["featured_image"],
        }

        products.append(product)

    return products
