import React, { useState } from "react";
import api from "../api/api";
import { useNavigate, Link } from "react-router-dom";

const RegisterPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleRegister = async () => {
    if (!email.trim() || !password.trim()) {
      setError("Пожалуйста, заполните все поля");
      setSuccess("");
      return;
    }
    if (password.length < 6) {
      setError("Пароль должен быть не менее 6 символов");
      setSuccess("");
      return;
    }

    try {
      await api.post("/auth/register", { email, password });
      setSuccess("Регистрация успешна! Теперь вы можете войти.");
      navigate("/login")
      setError("");
      setEmail("");
      setPassword("");
    } catch (err) {
      setError(err.response?.data?.detail || "Ошибка при регистрации");
      setSuccess("");
    }
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        height: "100vh",
        backgroundColor: "#f0f2f5",
        fontFamily: "'Inter', sans-serif",
        padding: "0 20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: 450,
          backgroundColor: "#fff",
          padding: "50px 40px",
          borderRadius: 14,
          boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
          textAlign: "center",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 20,
        }}
      >
        <h1 style={{ fontSize: 34, marginBottom: 10, color: "#333" }}>Создать аккаунт</h1>
    
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
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
            e.currentTarget.style.boxShadow = "0 0 8px rgba(25,118,210,0.2)";
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = "#ccc";
            e.currentTarget.style.boxShadow = "none";
          }}
        />
        <input
          type="password"
          placeholder="Пароль (не менее 6 символов)"
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
            e.currentTarget.style.boxShadow = "0 0 8px rgba(25,118,210,0.2)";
          }}
          onBlur={(e) => {
            e.currentTarget.style.borderColor = "#ccc";
            e.currentTarget.style.boxShadow = "none";
          }}
        />

        <button
          onClick={handleRegister}
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
            e.currentTarget.style.boxShadow = "0 6px 20px rgba(25,118,210,0.4)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = "none";
          }}
        >
          Зарегистрироваться
        </button>

        {error && <p style={{ color: "red", marginTop: 10 }}>{error}</p>}
        {success && <p style={{ color: "green", marginTop: 10 }}>{success}</p>}

        <p style={{ fontSize: 14, color: "#666", marginTop: 10 }}>
          Уже есть аккаунт?{" "}
          <Link to="/login" style={{ color: "#1976d2", textDecoration: "none" }}>
            Войти
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
