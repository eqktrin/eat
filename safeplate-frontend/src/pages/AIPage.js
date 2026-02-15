import React, { useState, useEffect } from "react";
import api from "../api/api";

const AIPage = () => {
  const [query, setQuery] = useState("");
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(false);
  const [userAllergens, setUserAllergens] = useState([]);
  const [reason, setReason] = useState("");

  // Получаем аллергены пользователя
  const fetchUserAllergens = async () => {
    try {
      const userRes = await api.get(`/profile/me`);
      setUserAllergens(userRes.data.allergens || []);
    } catch (err) {
      console.error("Ошибка при получении аллергенов:", err);
    }
  };

  const handleSearch = async () => {
    if (!query.trim()) return;
    setLoading(true);

    try {
      const userRes = await api.get(`/profile/me`);
      const userId = userRes.data.id;
      
      const res = await api.post("ai/query", {
        query: query,
        user_id: userId
      });
      setDishes(res.data.dishes || []);
      setReason(res.data.reason || "");
    } catch (err) {
      console.error("Ошибка при AI-поиске:", err);
    }

    setLoading(false);
  };

  // Проверяем, есть ли у блюда аллергены пользователя
  const hasDangerousAllergens = (dishAllergens) => {
    return dishAllergens.some(allergen => userAllergens.includes(allergen));
  };

  const handleFavorite = async (dish) => {
    try {
      await api.post(`/favorites/add`, { dish_id: dish.id });
      alert(`${dish.name} добавлено в избранное`);
    } catch (err) {
      console.error("Ошибка при добавлении в избранное:", err);
    }
  };

  const handleOrder = async (dish) => {
    if (hasDangerousAllergens(dish.allergens || [])) {
      alert("Это блюдо содержит ваши аллергены! Заказ невозможен.");
      return;
    }
    
    try {
      const userRes = await api.get(`/profile/me`);
      const userId = userRes.data.id;
      
      await api.post(`/orders/`, { dish_id: dish.id, user_id: userId });
      alert(`Заказ "${dish.name}" оформлен!`);
    } catch (err) {
      console.error("Ошибка при заказе:", err);
      alert("Ошибка при оформлении заказа");
    }
  };

  useEffect(() => {
    fetchUserAllergens();
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
      <h1
        style={{
          fontSize: 32,
          fontWeight: 700,
          marginBottom: 30,
          color: "#333",
        }}
      >
        AI поиск блюд
      </h1>

      {/* Блок с аллергенами пользователя */}
      {userAllergens.length > 0 && (
        <div style={{
          background: "#f8f9fa",
          padding: "15px 20px",
          borderRadius: 8,
          marginBottom: 25,
          border: "1px solid #dee2e6"
        }}>
          <strong style={{ color: "#333" }}>Ваши аллергены:</strong>
          <div style={{ marginTop: 10, display: "flex", flexWrap: "wrap", gap: 8 }}>
            {userAllergens.map((allergen, idx) => (
              <span key={idx} style={{
                background: "#e9ecef",
                color: "#495057",
                padding: "6px 12px",
                borderRadius: 20,
                fontSize: 14,
                fontWeight: 500,
              }}>
                {allergen}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Поисковая строка */}
      <div style={{ display: "flex", alignItems: "center", marginBottom: 30 }}>
        <input
          type="text"
          placeholder="Введите запрос, например: 'сладкое', 'веганское', 'быстрое'"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          style={{
            flex: 1,
            padding: "12px 16px",
            borderRadius: 8,
            border: "1px solid #ccc",
            fontSize: 16,
            outline: "none",
            transition: "0.2s border-color",
          }}
          onFocus={(e) => (e.currentTarget.style.borderColor = "#1976d2")}
          onBlur={(e) => (e.currentTarget.style.borderColor = "#ccc")}
        />

        <button
          onClick={handleSearch}
          style={{
            marginLeft: 12,
            padding: "12px 20px",
            borderRadius: 8,
            border: "none",
            background: "#1976d2",
            color: "#fff",
            fontWeight: 600,
            cursor: "pointer",
            fontSize: 16,
            transition: "0.3s transform, 0.3s box-shadow",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "scale(1.05)";
            e.currentTarget.style.boxShadow = "0 6px 20px rgba(25,118,210,0.5)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = "none";
          }}
          disabled={loading}
        >
          {loading ? "Поиск..." : "Найти"}
        </button>
      </div>

      {/* Примеры запросов */}
      <div style={{
        marginBottom: 30,
        padding: 20,
        background: "#f8f9fa",
        borderRadius: 8,
      }}>
        <p style={{ margin: "0 0 15px 0", color: "#666" }}>
          Примеры запросов:
        </p>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
          {['сладкое', 'полезное', 'быстрое', 'веганское', 'мясное'].map((text, idx) => (
            <span 
              key={idx}
              onClick={() => {
                setQuery(text);
                setTimeout(() => handleSearch(), 100);
              }}
              style={{
                background: "white",
                color: "#1976d2",
                padding: "8px 16px",
                borderRadius: 20,
                fontSize: 14,
                cursor: "pointer",
                transition: "0.2s all",
                border: "1px solid #1976d2",
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = "#1976d2";
                e.currentTarget.style.color = "white";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = "white";
                e.currentTarget.style.color = "#1976d2";
              }}
            >
              {text}
            </span>
          ))}
        </div>
      </div>

      {/* Результат поиска */}
      {reason && (
        <div style={{
          background: "#e3f2fd",
          padding: 15,
          borderRadius: 8,
          marginBottom: 25,
          borderLeft: "4px solid #1976d2"
        }}>
          <p style={{ margin: 0, color: "#1565c0", fontSize: 15 }}>
            {reason}
          </p>
        </div>
      )}

      {loading && (
        <p style={{ 
          textAlign: "center", 
          padding: 40,
          color: "#555",
          fontStyle: "italic" 
        }}>
          Идёт поиск...
        </p>
      )}

      <div style={{ marginTop: 30 }}>
        {dishes.length === 0 && !loading && query && (
          <p style={{ 
            textAlign: "center", 
            padding: 40,
            color: "#777" 
          }}>
            Ничего не найдено по запросу "{query}"
          </p>
        )}

        {dishes.map((dish, index) => {
          const isDangerous = hasDangerousAllergens(dish.allergens || []);
          const hasAllergens = dish.allergens && dish.allergens.length > 0;
          
          return (
            <div
              key={dish.id}
              style={{
                border: isDangerous ? "2px solid #d32f2f" : 
                       hasAllergens ? "1px solid #ffb74d" : "1px solid #e0e0e0",
                padding: 20,
                marginBottom: 20,
                borderRadius: 12,
                boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
                transition: "0.3s transform, 0.3s box-shadow",
                opacity: 0,
                transform: "translateY(20px)",
                animation: `fadeInUp 0.5s ease forwards`,
                animationDelay: `${index * 0.1}s`,
                background: isDangerous ? "#fff5f5" : 
                           hasAllergens ? "#fffaf0" : "white"
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = "translateY(-3px)";
                e.currentTarget.style.boxShadow = "0 6px 20px rgba(0,0,0,0.1)";
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = "translateY(0)";
                e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.05)";
              }}
            >
              <div style={{ 
                display: "flex", 
                justifyContent: "space-between",
                alignItems: "flex-start",
                marginBottom: 12 
              }}>
                <h3 style={{ 
                  margin: "0 0 8px 0", 
                  color: "#333",
                  fontSize: 20,
                  fontWeight: 600,
                  flex: 1 
                }}>
                  {dish.name}
                </h3>
                
                {isDangerous ? (
                  <span style={{
                    padding: "4px 10px",
                    borderRadius: 4,
                    fontSize: 12,
                    fontWeight: 600,
                    background: "#ffebee",
                    color: "#d32f2f",
                    marginLeft: 10
                  }}>
                    Опасно
                  </span>
                ) : hasAllergens ? (
                  <span style={{
                    padding: "4px 10px",
                    borderRadius: 4,
                    fontSize: 12,
                    fontWeight: 600,
                    background: "#fff3e0",
                    color: "#ef6c00",
                    marginLeft: 10
                  }}>
                    Аллергены
                  </span>
                ) : (
                  <span style={{
                    padding: "4px 10px",
                    borderRadius: 4,
                    fontSize: 12,
                    fontWeight: 600,
                    background: "#e8f5e9",
                    color: "#2e7d32",
                    marginLeft: 10
                  }}>
                    Безопасно
                  </span>
                )}
              </div>
              
              <p style={{ 
                margin: "0 0 15px 0", 
                color: "#555",
                lineHeight: 1.5 
              }}>
                {dish.description}
              </p>

              <div style={{ marginBottom: 15 }}>
                <strong style={{ 
                  display: "block", 
                  marginBottom: 8, 
                  color: "#333" 
                }}>
                  Аллергены:
                </strong>
                {dish.allergens.length > 0 ? (
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
                    {dish.allergens.map((a, idx) => {
                      const isDanger = userAllergens.includes(a);
                      return (
                        <span 
                          key={idx} 
                          style={{
                            background: isDanger ? "#ffebee" : "#fff3e0",
                            color: isDanger ? "#d32f2f" : "#ef6c00",
                            padding: "4px 10px",
                            borderRadius: 4,
                            fontSize: 13,
                            fontWeight: 500,
                          }}
                        >
                          {a}
                        </span>
                      );
                    })}
                  </div>
                ) : (
                  <span style={{ color: "#777", fontStyle: "italic" }}>
                    Нет аллергенов
                  </span>
                )}
              </div>

              {isDangerous && (
                <div style={{
                  background: "#ffebee",
                  color: "#d32f2f",
                  padding: "10px 12px",
                  borderRadius: 6,
                  margin: "15px 0",
                  fontSize: 14,
                  fontWeight: 500,
                  borderLeft: "3px solid #d32f2f"
                }}>
                  Содержит ваши аллергены
                </div>
              )}

              <div style={{ 
                display: "flex", 
                gap: 12,
                marginTop: 15 
              }}>
                <button
                  onClick={() => handleOrder(dish)}
                  style={{
                    flex: 1,
                    padding: "10px 16px",
                    borderRadius: 8,
                    border: "none",
                    background: isDangerous ? "#f5f5f5" : "#1976d2",
                    color: isDangerous ? "#9e9e9e" : "#fff",
                    fontWeight: 600,
                    cursor: isDangerous ? "not-allowed" : "pointer",
                    fontSize: 14,
                    transition: "0.3s transform, 0.3s box-shadow",
                  }}
                  onMouseEnter={(e) => {
                    if (!isDangerous) {
                      e.currentTarget.style.transform = "scale(1.05)";
                      e.currentTarget.style.boxShadow = "0 6px 20px rgba(25,118,210,0.5)";
                    }
                  }}
                  onMouseLeave={(e) => {
                    if (!isDangerous) {
                      e.currentTarget.style.transform = "scale(1)";
                      e.currentTarget.style.boxShadow = "none";
                    }
                  }}
                >
                  {isDangerous ? "Недоступно" : "Заказать"}
                </button>
                
                <button
                  onClick={() => handleFavorite(dish)}
                  style={{
                    padding: "10px 16px",
                    background: "#fff",
                    color: "#1976d2",
                    border: "1px solid #1976d2",
                    borderRadius: 8,
                    fontSize: 14,
                    fontWeight: 600,
                    cursor: "pointer",
                    transition: "0.3s transform, 0.3s box-shadow",
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = "scale(1.05)";
                    e.currentTarget.style.boxShadow = "0 6px 20px rgba(25,118,210,0.3)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = "scale(1)";
                    e.currentTarget.style.boxShadow = "none";
                  }}
                >
                  В избранное
                </button>
              </div>
            </div>
          );
        })}
      </div>

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

export default AIPage;