import React, { useEffect, useState } from "react";
import api from "../api/api";

const MenuPage = () => {
  const [dishes, setDishes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");
  const [userAllergens, setUserAllergens] = useState([]);
  const [showAll, setShowAll] = useState(false);

  const fetchUserAllergens = async () => {
    try {
      const userRes = await api.get(`/profile/me`);
      setUserAllergens(userRes.data.allergens || []);
    } catch (err) {
      console.error("Ошибка при получении аллергенов:", err);
    }
  };

  const fetchDishes = async () => {
    setLoading(true);
    try {
      const res = await api.get("/menu/");
      setDishes(res.data || []);
    } catch (err) {
      console.error("Ошибка при получении блюд:", err);
    }
    setLoading(false);
  };

  const handleFavorite = async (dish) => {
    try {
      await api.post(`/favorites/add`, {
        dish_id: dish.id,
      });
      alert(`${dish.name} добавлено в избранное`);
    } catch (err) {
      console.error("Ошибка при добавлении в избранное:", err);
    }
  };

  const handleOrder = async (dish) => {
    const isDangerous = dish.allergens.some(a => userAllergens.includes(a));
    
    if (isDangerous) {
      alert("Это блюдо содержит ваши аллергены! Заказ невозможен.");
      return;
    }
    
    try {
      const userRes = await api.get(`/profile/me`);
      const userId = userRes.data.id;
      
      await api.post(`/orders/`, {
        dish_id: dish.id,
        user_id: userId
      });
      alert(`Заказ "${dish.name}" оформлен!`);
    } catch (err) {
      console.error("Ошибка при заказе:", err);
      alert("Ошибка при оформлении заказа");
    }
  };

  // Фильтрация блюд по аллергенам (безопасные блюда)
  const safeDishes = dishes.filter(
    (d) => !d.allergens.some((a) => userAllergens.includes(a))
  );

  // Поиск по названию
  const displayedDishes = (showAll ? dishes : safeDishes).filter((d) =>
    d.name.toLowerCase().includes(search.toLowerCase())
  );

  // Статистика
  const dangerousDishes = dishes.filter(d => 
    d.allergens.some(a => userAllergens.includes(a))
  );

  useEffect(() => {
    fetchUserAllergens();
    fetchDishes();
  }, []);

  return (
    <div
      style={{
        padding: "40px 20px",
        maxWidth: 800,
        margin: "0 auto",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 30, color: "#333" }}>
        Меню
      </h1>

      {/* Статистика и фильтры */}
      <div style={{
        background: "#f8f9fa",
        padding: 20,
        borderRadius: 8,
        marginBottom: 25,
        border: "1px solid #dee2e6"
      }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 15 }}>
          <div>
            <strong>Статистика:</strong>
            <span style={{ marginLeft: 15, color: "#2e7d32" }}>Безопасно: {safeDishes.length}</span>
            <span style={{ marginLeft: 15, color: "#d32f2f" }}>Опасно: {dangerousDishes.length}</span>
            <span style={{ marginLeft: 15, color: "#555" }}>Всего: {dishes.length}</span>
          </div>
          
          <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
            <input
              type="checkbox"
              checked={showAll}
              onChange={(e) => setShowAll(e.target.checked)}
              style={{ width: 18, height: 18 }}
            />
            <span>Показывать все блюда</span>
          </label>
        </div>
        
        {userAllergens.length > 0 && (
          <div>
            <strong>Ваши аллергены:</strong>
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
      </div>

      {/* Поиск */}
      <input
        type="text"
        placeholder="Поиск по названию..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{
          width: "100%",
          padding: 12,
          marginBottom: 30,
          borderRadius: 8,
          border: "1px solid #ccc",
          fontSize: 16,
          outline: "none",
          transition: "0.2s border-color",
        }}
        onFocus={(e) => (e.currentTarget.style.borderColor = "#1976d2")}
        onBlur={(e) => (e.currentTarget.style.borderColor = "#ccc")}
      />

      {/* Предупреждение */}
      {dangerousDishes.length > 0 && !showAll && (
        <div style={{
          background: "#fff5f5",
          border: "1px solid #ffcdd2",
          color: "#d32f2f",
          padding: 15,
          borderRadius: 8,
          marginBottom: 25,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center"
        }}>
          <span>
            <strong>Внимание!</strong> В меню есть {dangerousDishes.length} блюд, содержащих ваши аллергены.
          </span>
          <button
            onClick={() => setShowAll(true)}
            style={{
              padding: "8px 16px",
              background: "#d32f2f",
              color: "white",
              border: "none",
              borderRadius: 6,
              cursor: "pointer",
              fontWeight: 600,
              fontSize: 14
            }}
          >
            Показать все
          </button>
        </div>
      )}

      {/* Список блюд */}
      {loading ? (
        <p style={{ textAlign: "center", padding: 40, color: "#555" }}>Загрузка...</p>
      ) : displayedDishes.length === 0 ? (
        <p style={{ textAlign: "center", padding: 40, color: "#777" }}>Нет доступных блюд</p>
      ) : (
        displayedDishes.map((dish) => {
          const isDangerous = dish.allergens.some(a => userAllergens.includes(a));
          const hasAllergens = dish.allergens.length > 0;
          
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
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <h3 style={{ fontSize: 20, fontWeight: 600, marginBottom: 8, color: "#333" }}>
                  {dish.name}
                </h3>
                {isDangerous ? (
                  <span style={{
                    padding: "4px 10px",
                    borderRadius: 4,
                    fontSize: 12,
                    fontWeight: 600,
                    background: "#ffebee",
                    color: "#d32f2f"
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
                    color: "#ef6c00"
                  }}>
                    Аллергены
                  </span>
                ) : null}
              </div>
              
              <p style={{ color: "#555", marginBottom: 12 }}>{dish.description}</p>

              <div style={{ marginBottom: 15 }}>
                <strong>Аллергены:</strong>
                {dish.allergens.length > 0 ? (
                  <div style={{ marginTop: 8, display: "flex", flexWrap: "wrap", gap: 8 }}>
                    {dish.allergens.map((a) => {
                      const isDanger = userAllergens.includes(a);
                      return (
                        <span 
                          key={a} 
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
                  <span style={{ color: "#777", fontStyle: "italic", marginLeft: 10 }}>Нет аллергенов</span>
                )}
              </div>

              {isDangerous && (
                <div style={{
                  background: "#ffebee",
                  color: "#d32f2f",
                  padding: "10px 12px",
                  borderRadius: 6,
                  margin: "10px 0 15px 0",
                  fontSize: 14,
                  fontWeight: 500,
                  borderLeft: "3px solid #d32f2f"
                }}>
                  Содержит ваши аллергены
                </div>
              )}

              <div style={{ display: "flex", gap: 12 }}>
                <button
                  onClick={() => handleOrder(dish)}
                  style={{
                    padding: "10px 16px",
                    backgroundColor: isDangerous ? "#f5f5f5" : "#1976d2",
                    color: isDangerous ? "#9e9e9e" : "#fff",
                    border: "none",
                    borderRadius: 8,
                    cursor: isDangerous ? "not-allowed" : "pointer",
                    fontWeight: 600,
                    transition: "0.3s transform, 0.3s box-shadow",
                    flex: 1
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
                    backgroundColor: "#fff",
                    color: "#1976d2",
                    border: "1px solid #1976d2",
                    borderRadius: 8,
                    cursor: "pointer",
                    fontWeight: 600,
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
        })
      )}
    </div>
  );
};

export default MenuPage;