import React, { useEffect, useState } from "react";
import { fetchOutfits } from "./api";
import BaseProduct from "./components/BaseProduct";
import OutfitGrid from "./components/OutfitGrid";
import "./styles.css";

export default function App() {
  const [data, setData] = useState(null);
  const [activeIndex, setActiveIndex] = useState(0);

  useEffect(() => {
    fetchOutfits("WBP1113BA0000").then(setData);
  }, []);

  if (!data) return <div className="loading">Loading outfits...</div>;

  return (
    <div className="container">
      <BaseProduct product={data.base_product} />

      <div className="right-panel">
        <div className="outfit-tabs">
          {data.outfits.map((_, i) => (
            <button
              key={i}
              className={i === activeIndex ? "active" : ""}
              onClick={() => setActiveIndex(i)}
            >
              Outfit {i + 1}
            </button>
          ))}
        </div>

        <OutfitGrid outfits={[data.outfits[activeIndex]]} />
      </div>
    </div>
  );
}
