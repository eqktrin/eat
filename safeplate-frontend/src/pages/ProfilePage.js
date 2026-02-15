import React, { useEffect, useState } from "react";
import api from "../api/api";
import { useNavigate } from "react-router-dom";

const ProfilePage = () => {
  const navigate = useNavigate();
  const userId = localStorage.getItem("user_id") || 1;

  const [user, setUser] = useState({ email: "", allergens: [] });
  const [loading, setLoading] = useState(false);
  const [newAllergen, setNewAllergen] = useState("");

  const fetchProfile = async () => {
    setLoading(true);
    try {
      const userRes = await api.get(`/profile/me`);  // ← НОВЫЙ ПУТЬ!
      // ИСПРАВЛЕНО: используем setUser вместо setUserAllergens
      setUser({
        email: userRes.data.email,
        allergens: userRes.data.allergens || []
      });
    } catch (err) {
      console.error("Ошибка при получении профиля:", err);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleAddAllergen = async () => {
    if (!newAllergen.trim()) return;

    const updatedAllergens = [...user.allergens, newAllergen.trim()];
    try {
      // ИСПРАВЛЕНО: убрал user_id из запроса
      await api.post("/allergens/update", {
        allergens: updatedAllergens,  // ← ТОЛЬКО allergens!
      });
      setUser({ ...user, allergens: updatedAllergens });
      setNewAllergen("");
    } catch (err) {
      console.error("Ошибка при обновлении аллергенов:", err);
    }
  };

  const handleRemoveAllergen = async (allergen) => {
    const updatedAllergens = user.allergens.filter((a) => a !== allergen);
    try {
      await api.post("/allergens/update", {
        allergens: updatedAllergens,  
      });
      setUser({ ...user, allergens: updatedAllergens });
    } catch (err) {
      console.error("Ошибка при удалении аллергена:", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("user_id");
    localStorage.removeItem("access_token"); 
    sessionStorage.clear();          

    delete api.defaults.headers.common["Authorization"];

    navigate("/login");
    window.location.reload(); 
  };

  return (
    <div
      style={{
        padding: "40px 20px",
        minHeight: "100vh",
        fontFamily: "'Inter', sans-serif",
        backgroundColor: "#f5f5f5",
      }}
    >
      <div
        style={{
          maxWidth: 650,
          margin: "0 auto",
        }}
      >
        {/* Заголовок и кнопка выхода */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: 30,
          }}
        >
          <h1 style={{ fontSize: 32, fontWeight: 700, color: "#333" }}>
            Профиль
          </h1>
          <button
            onClick={handleLogout}
            style={{
              padding: "8px 16px",
              backgroundColor: "#e53935",
              color: "#fff",
              border: "none",
              borderRadius: 20,
              cursor: "pointer",
              fontWeight: 600,
              transition: "0.3s transform, 0.3s box-shadow",
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = "scale(1.05)";
              e.currentTarget.style.boxShadow =
                "0 6px 20px rgba(229,57,53,0.4)";
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = "scale(1)";
              e.currentTarget.style.boxShadow = "none";
            }}
          >
            Выйти
          </button>
        </div>

        {loading ? (
          <p>Загрузка...</p>
        ) : (
          <>
            {/* Блок с информацией */}
            <div
              style={{
                background: "#fff",
                padding: 25,
                borderRadius: 20,
                boxShadow: "0 4px 20px rgba(0,0,0,0.05)",
                marginBottom: 25,
              }}
            >
              <p style={{ fontSize: 18 }}>
                <strong>Email:</strong> {user.email}
              </p>
              <p style={{ color: "#555", marginTop: 8 }}>
                Здесь вы можете управлять своими аллергенами и получать
                персонализированные рекомендации.
              </p>
            </div>

            {/* Блок с аллергенами */}
            <div
              style={{
                background: "#fff",
                padding: 25,
                borderRadius: 20,
                boxShadow: "0 4px 20px rgba(0,0,0,0.05)",
              }}
            >
              <h3 style={{ marginBottom: 15 }}>Аллергены</h3>
              {user.allergens.length === 0 ? (
                <p style={{ color: "#777" }}>Список пуст</p>
              ) : (
                <ul style={{ listStyle: "none", paddingLeft: 0, marginBottom: 20 }}>
                  {user.allergens.map((a) => (
                    <li
                      key={a}
                      style={{
                        marginBottom: 10,
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center",
                        padding: "6px 12px",
                        borderRadius: 12,
                        background: "#f0f0f0",
                      }}
                    >
                      <span>{a}</span>
                      <button
                        onClick={() => handleRemoveAllergen(a)}
                        style={{
                          padding: "4px 8px",
                          backgroundColor: "#e53935",
                          color: "#fff",
                          border: "none",
                          borderRadius: 12,
                          cursor: "pointer",
                          fontSize: 14,
                          transition: "0.2s transform, 0.2s box-shadow",
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = "scale(1.05)";
                          e.currentTarget.style.boxShadow =
                            "0 4px 12px rgba(229,57,53,0.3)";
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = "scale(1)";
                          e.currentTarget.style.boxShadow = "none";
                        }}
                      >
                        Удалить
                      </button>
                    </li>
                  ))}
                </ul>
              )}

              <div style={{ display: "flex", gap: 10 }}>
                <input
                  type="text"
                  placeholder="Новый аллерген"
                  value={newAllergen}
                  onChange={(e) => setNewAllergen(e.target.value)}
                  style={{
                    flex: 1,
                    padding: 12,
                    borderRadius: 12,
                    border: "1px solid #ccc",
                    fontSize: 16,
                    outline: "none",
                    transition: "0.2s border-color",
                  }}
                  onFocus={(e) =>
                    (e.currentTarget.style.borderColor = "#1976d2")
                  }
                  onBlur={(e) => (e.currentTarget.style.borderColor = "#ccc")}
                />
                <button
                  onClick={handleAddAllergen}
                  style={{
                    padding: "10px 16px",
                    backgroundColor: "#1976d2",
                    color: "#fff",
                    border: "none",
                    borderRadius: 12,
                    cursor: "pointer",
                    fontWeight: 600,
                    transition: "0.3s transform, 0.3s box-shadow",
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = "scale(1.05)";
                    e.currentTarget.style.boxShadow =
                      "0 6px 20px rgba(25,118,210,0.4)";
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = "scale(1)";
                    e.currentTarget.style.boxShadow = "none";
                  }}
                >
                  Добавить
                </button>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default ProfilePage;
