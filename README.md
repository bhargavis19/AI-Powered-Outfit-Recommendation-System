# 🧠 AI-Powered Outfit Recommendation System

## 📌 Project Overview

This project implements an **AI-powered Outfit Recommendation System** that generates **complete outfit combinations** using a **single base product** as input.

Given a product (e.g., a watch, top, or footwear), the system simulates how a **human fashion stylist** would assemble outfits by reasoning over:

- Color harmony  
- Style compatibility  
- Occasion appropriateness  
- Budget alignment  
- Outfit completeness  

The focus of this project is **system design, reasoning quality, and performance**, not UI polish or heavy ML models.

---

## 🏗️ System Architecture

```
├── app/
│   ├── main.py          # FastAPI app & API routes
│   ├── data_loader.py   # Product ingestion & attribute inference
│   ├── recommender.py   # Stylist-driven outfit generation logic
│   ├── scoring.py       # Weighted outfit scoring
│   └── cache.py         # Optional in-memory cache
│
├── data/
│   └── products.xlsx    # Product catalog
│
├── requirements.txt
└── README.md
```

---

## 🔄 Data Flow

1. Product catalog is loaded once at startup  
2. API receives a `base_product_id`  
3. Candidate products are filtered in-memory  
4. Compatible outfit combinations are assembled  
5. Each outfit is scored and ranked  
6. Response is returned in **< 1 second**  

---

## 📊 Data Modeling

The raw product catalog (`products.xlsx`) contains real-world e-commerce fields such as:

- `sku_id`
- `title`
- `category`, `sub_category`, `product_type`
- `gender`
- `tags`, `description`
- `lowest_price`
- `featured_image`

---

## 🔍 Derived Attributes

Fashion attributes are inferred using **lightweight NLP heuristics** over product text:

- Color  
- Style  
- Occasion  
- Season  

Each product is normalized into the following schema:

```json
{
  "id": "string",
  "name": "string",
  "category": "top | bottom | footwear | accessory",
  "gender": "men | women | unisex",
  "colors": [],
  "style": [],
  "occasion": [],
  "season": [],
  "price": number,
  "brand": "string",
  "image": "url"
}
```

---

## 🧠 Recommendation Logic (Stylist Thinking)

### 1️⃣ Base Product Context

The base product defines the styling context, including:

- Gender  
- Style  
- Occasion  
- Color palette  
- Price range  

Accessories (e.g., watches) act as **anchors** and are **never duplicated**.

---

### 2️⃣ Candidate Filtering (Fast Pre-Filters)

Products are filtered using:

- Gender compatibility  
- Occasion overlap  
- Price range (±40%)  
- Category constraints  

This removes **~70–80%** of items before deeper reasoning.

---

### 3️⃣ Compatibility Rules

#### 🎨 Color Compatibility
- Neutral colors always compatible  
- Shared accent colors preferred  
- Too many conflicting accents penalized  

#### 👕 Style Compatibility
- Athleisure ↔ Casual allowed  
- Street ↔ Street only  
- Formal isolated  

#### 🎯 Occasion Compatibility
- Prevents mismatches (e.g., workout ≠ formal)  

All rules are **deterministic and explainable**.

---

### 4️⃣ Outfit Assembly Rules

Each outfit must include:

- Top  
- Bottom  
- Footwear  
- Exactly **one accessory**  

#### Primary Path
```
Top + Bottom + Footwear + Accessory
```

#### Fallback Paths (Graceful Degradation)
```
Top + Bottom + Accessory
Top + Footwear + Accessory
```

Rules enforced:

- No repeated items  
- No duplicate accessories (e.g., two watches)  
- Each outfit is visibly distinct  

---

## 📈 Scoring System

Each outfit receives a `match_score ∈ [0, 1]` using a weighted heuristic model:

```
match_score =
0.35 × color_score +
0.30 × style_score +
0.20 × occasion_score +
0.15 × budget_score
```

### Scoring Components

- **Color Score** – Measures harmony between base product and outfit items  
- **Style Score** – Rewards stylistically consistent combinations  
- **Occasion Score** – Ensures appropriate usage alignment  
- **Budget Score** – Penalizes extreme price mismatches  

All scoring is:

- Deterministic  
- Explainable  
- Computed fully in-memory  

---

## ⚡ Performance Strategy

- Product catalog preloaded at startup  
- No database queries at runtime  
- No ML inference or external APIs  
- Pure in-memory filtering and scoring  
- Optional request-level caching  
- Request-level caching implemented using an in-memory dictionary keyed by base product ID

---

## ⏱ Performance Benchmark

| Scenario | Avg Response Time |
|--------|-------------------|
| Cold start | ~120 ms |
| Warm cache | ~20–30 ms |
| Worst case | < 200 ms |

---

## 🔌 API Interface

### Endpoint
```
POST /recommend-outfits
```

### Parameters

| Parameter | Type | Description |
|--------|------|-------------|
| base_product_id | string | SKU of base product |
| max_outfits | integer | Number of outfits |

### Sample Request

```json
{
  "base_product_id": "WBP1113BA0000",
  "max_outfits": 3
}
```

### Sample Response (Truncated)

```json
{
  "base_product": {},
  "outfits": [
    {
      "items": {
        "top": {},
        "bottom": {},
        "footwear": {},
        "accessory": {}
      },
      "match_score": 0.78,
      "explanation": {
        "color": "Balanced color harmony",
        "style": "Consistent styling",
        "occasion": "Appropriate usage",
        "budget": "Price-aligned"
      }
    }
  ]
}
```

---

---

## 🖥️ Frontend Interface (Minimal UI)

A lightweight React (Vite) frontend is included to visually demonstrate the recommendations.

### Design Principles
- Minimal and distraction-free
- Reference-aligned layout
- Focus on outfit grouping and clarity
- No business logic on frontend

### Features
- Base product hero display
- Dynamic outfit switching (tabs)
- Grouped outfit cards
- Responsive layout (desktop → mobile)
- API-driven rendering

The frontend acts purely as a **presentation layer**, with all recommendation logic handled by the backend.

---

## ▶️ How to Run Locally

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Swagger UI
```
http://127.0.0.1:8000/docs
```

---

## 🎥 Demo

A short walkthrough video demonstrates:
- API usage via Swagger
- Outfit generation logic
- Frontend rendering and responsiveness
- Match score explanation

(Alternatively, the system can be tested directly using the provided API endpoint.)

---

## 🧪 Testing

Tested with:

- Accessories (watches)  
- Clothing  
- Footwear  

✅ All scenarios return **valid, complete outfits**.

---

## 🤖 AI Usage Explanation

This system follows a **hybrid AI approach**:

- Rule-based reasoning  
- Weighted heuristic scoring  

LLMs are intentionally **not used** to guarantee:

- Low latency  
- Predictable behavior  
- Cost efficiency  
- Extensibility  

An LLM-based explanation or personalization layer can be added asynchronously without impacting core performance.

---

## ⚖️ Assumptions & Trade-offs

### Assumptions
- Catalog may be sparse  
- Missing attributes should not block recommendations  

### Trade-offs
- Heuristics over ML models  
- Simplicity over learned ranking  
- In-memory data over persistent databases  

---

## 🚀 Future Improvements

- ML-based color harmony  
- User personalization  
- Advanced budget constraints  
- Image similarity  
- Redis caching  

---

## 📌 Conclusion

This project demonstrates a **production-minded, fast, and explainable outfit recommendation system** that balances:

- Stylist-level reasoning  
- System performance  
- Maintainability  
- Real-world constraints  
