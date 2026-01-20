export async function fetchOutfits(baseProductId) {
  const res = await fetch(
    `http://127.0.0.1:8000/recommend-outfits?base_product_id=${baseProductId}&max_outfits=3`,
    { method: "POST" }
  );
  return res.json();
}
