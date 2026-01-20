import React from "react";

export default function BaseProduct({ product }) {
  return (
    <div className="base-product">
      <img src={product.image} alt={product.name} />
      <h2>{product.name}</h2>
      <p className="brand">{product.brand}</p>
    </div>
  );
}
