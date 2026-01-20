import React from "react";
import ProductCard from "./ProductCard";

export default function OutfitCard({ outfit }) {
  return (
    <div className="outfit-card">
      <div className="products">
        {Object.values(outfit.items).map((item) => (
          <ProductCard key={item.id} product={item} />
        ))}
      </div>

      <div className="score">
        Match Score: {(outfit.match_score * 100).toFixed(0)}%
      </div>

    </div>
  );
}
