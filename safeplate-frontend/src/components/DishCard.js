import React from "react";

const DishCard = ({ dish }) => {
  return (
    <div style={{
      border: "1px solid #ccc",
      padding: "12px",
      borderRadius: "8px",
      width: "200px"
    }}>
      <h3>{dish.name}</h3>
      <p>{dish.description}</p>
      {dish.allergens.length > 0 && (
        <p style={{ color: "red" }}>Аллергены: {dish.allergens.join(", ")}</p>
      )}
    </div>
  );
};

export default DishCard;

