from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.data_loader import load_products
from app.recommender import generate_outfits
from app.cache import get_cached, set_cached

app = FastAPI(title="AI Outfit Recommendation System")

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load data once
products = load_products()
product_map = {p["id"]: p for p in products}

@app.post("/recommend-outfits")
def recommend(base_product_id: str, max_outfits: int = 3):
    if base_product_id not in product_map:
        raise HTTPException(status_code=404, detail="Product not found")

    cached = get_cached(base_product_id)
    if cached:
        return cached

    base = product_map[base_product_id]
    outfits = generate_outfits(base, products, max_outfits)

    response = {
        "base_product": base,
        "outfits": outfits
    }

    set_cached(base_product_id, response)
    return response
