import React from "react";
import OutfitCard from "./OutfitCard";

export default function OutfitGrid({ outfits }) {
  return (
    <div className="outfit-grid">
      {outfits.map((outfit, i) => (
        <OutfitCard key={i} outfit={outfit} />
      ))}
    </div>
  );
}
