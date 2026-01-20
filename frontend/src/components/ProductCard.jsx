import React from "react";

export default function ProductCard({ product }) {
  return (
    <div className="product-card">
      <img src={product.image} alt={product.name} />
      <p className="name">{product.name}</p>
      <p className="price">
        ₹{product.price > 0 ? product.price : "—"}
      </p>
    </div>
  );
}
