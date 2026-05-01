import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const LoginPage: React.FC = () => {
    const navigate = useNavigate();
    const { login } = useAuth();
    const [email, setEmail] = useState<string>("");
    const [password, setPassword] = useState<string>("");
    const [error, setError] = useState<string>("");

    const handleLogin = async (): Promise<void> => {
        if (!email.trim() || !password.trim()) {
            setError("Пожалуйста, заполните все поля");
            return;
        }
        try {
            await login(email, password);
            navigate("/profile");
        } catch (err) {
            setError("Неверный email или пароль");
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
                    alignItems: "center",
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

                <p style={{ fontSize: 14, color: "#666", marginTop: 10 }}>
                    Нет аккаунта?{" "}
                    <Link to="/register" style={{ color: "#1976d2", textDecoration: "none" }}>
                        Зарегистрироваться
                    </Link>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;