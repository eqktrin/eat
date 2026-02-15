import React, { useEffect, useState } from "react";
import api from "../api/api";

const FavoritesPage = () => {
  const [favorites, setFavorites] = useState([]);
  const [loading, setLoading] = useState(true);

  const fetchFavorites = async () => {
    setLoading(true);
    try {
      // ИЗМЕНИЛ: убрал user_id из пути
      const res = await api.get(`/favorites/my`);
      setFavorites(res.data || []);
    } catch (err) {
      console.error("Ошибка при получении избранного:", err);
    }
    setLoading(false);
  };

  const handleRemove = async (dishId) => {
    try {
      // ИЗМЕНИЛ: убрал user_id из запроса
      await api.post(`/favorites/remove`, { dish_id: dishId });
      setFavorites((prev) => prev.filter((d) => d.id !== dishId));
    } catch (err) {
      console.error("Ошибка при удалении из избранного:", err);
    }
  };

  useEffect(() => {
    fetchFavorites();
  }, []);

  return (
    <div
      style={{
        padding: "40px 20px",
        fontFamily: "'Inter', sans-serif",
        maxWidth: 900,
        margin: "0 auto",
      }}
    >
      <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 20, color: "#333" }}>
        Избранное
      </h1>

      {loading ? (
        <p style={{ color: "#555", fontStyle: "italic" }}>Загрузка...</p>
      ) : favorites.length === 0 ? (
        <p style={{ color: "#777" }}>Нет добавленных блюд</p>
      ) : (
        favorites.map((dish, index) => (
          <div
            key={dish.id}
            style={{
              border: "1px solid #eee",
              boxShadow: "0 4px 15px rgba(0,0,0,0.05)",
              padding: 20,
              marginBottom: 16,
              borderRadius: 12,
              opacity: 0,
              transform: "translateY(20px)",
              animation: `fadeInUp 0.5s ease forwards`,
              animationDelay: `${index * 0.1}s`,
            }}
          >
            <h3 style={{ margin: "0 0 8px 0", color: "#007bff" }}>{dish.name}</h3>
            <p style={{ margin: "0 0 12px 0", color: "#555" }}>{dish.description}</p>

            <strong style={{ display: "block", marginBottom: 6, color: "#333" }}>
              Аллергены:
            </strong>
            {dish.allergens.length > 0 ? (
              <ul style={{ margin: 0, paddingLeft: 20, color: "#777" }}>
                {dish.allergens.map((a) => (
                  <li key={a}>{a}</li>
                ))}
              </ul>
            ) : (
              <span style={{ color: "#777" }}>Нет</span>
            )}

            <button
              onClick={() => handleRemove(dish.id)}
              style={{
                marginTop: 12,
                padding: "8px 14px",
                backgroundColor: "#d32f2f",
                color: "#fff",
                border: "none",
                borderRadius: 8,
                cursor: "pointer",
                fontWeight: 600,
                transition: "0.3s transform, 0.3s box-shadow",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "scale(1.05)";
                e.currentTarget.style.boxShadow = "0 8px 20px rgba(211,47,47,0.4)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "scale(1)";
                e.currentTarget.style.boxShadow = "none";
              }}
            >
              Удалить
            </button>
          </div>
        ))
      )}

      {/* Анимация */}
      <style>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </div>
  );
};

export default FavoritesPage;
