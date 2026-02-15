import React, { useState } from "react";
import api from "../api/api";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const formData = new FormData();
        formData.append('username', email);
        formData.append('password', password);
        formData.append('grant_type', 'password');
        
        const response = await api.post("/auth/token", formData, {
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
        });
        
        // Сохраняем токен
        localStorage.setItem("access_token", response.data.access_token);
        localStorage.setItem("user_id", response.data.user_id);
        
        // Токен будет автоматически добавляться к будущим запросам
        // через interceptor в api.js
        navigate("/profile");
    } catch (error) {
        console.error("Ошибка входа:", error);
        alert("Неверный email или пароль");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#f5f5f5",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 400,
          backgroundColor: "#fff",
          padding: "50px 30px",
          borderRadius: 12,
          boxShadow: "0 8px 30px rgba(0,0,0,0.08)",
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center", // вот это центрирует поля
          gap: 20,
        }}
      >
        <h1 style={{ fontSize: 32, marginBottom: 20, color: "#333" }}>Вход</h1>

        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={{
            width: "80%", // оставляем отступы слева/справа
            padding: 14,
            fontSize: 16,
            borderRadius: 10,
            border: "1px solid #ccc",
            outline: "none",
            transition: "0.2s border-color, 0.2s box-shadow",
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = "#1976d2";
            e.currentTarget.style.boxShadow = "0 0 8px rgba(25,118,210,0.3)";
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = "#ccc";
            e.currentTarget.style.boxShadow = "none";
          }}
        />

        <input
          type="password"
          placeholder="Пароль"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{
            width: "80%",
            padding: 14,
            fontSize: 16,
            borderRadius: 10,
            border: "1px solid #ccc",
            outline: "none",
            transition: "0.2s border-color, 0.2s box-shadow",
          }}
          onFocus={(e) => {
            e.currentTarget.style.borderColor = "#1976d2";
            e.currentTarget.style.boxShadow = "0 0 8px rgba(25,118,210,0.3)";
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = "#ccc";
            e.currentTarget.style.boxShadow = "none";
          }}
        />

        <button
          onClick={handleLogin}
          style={{
            width: "50%",
            padding: "14px 0",
            backgroundColor: "#1976d2",
            color: "#fff",
            border: "none",
            borderRadius: 10,
            fontSize: 16,
            fontWeight: 600,
            cursor: "pointer",
            transition: "0.3s transform, 0.3s box-shadow",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "scale(1.03)";
            e.currentTarget.style.boxShadow = "0 6px 20px rgba(25,118,210,0.5)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          Войти
        </button>

        {error && (
          <p style={{ color: "red", marginTop: 20, fontWeight: 500 }}>{error}</p>
        )}
      </div>
    </div>
  );
};

export default LoginPage;
