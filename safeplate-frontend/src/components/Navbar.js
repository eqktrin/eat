import React, { useState, useEffect } from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const links = [
    { path: "/menu", label: "Меню" },
    { path: "/favorites", label: "Избранное" },
    { path: "/ai", label: "AI поиск" },
    { path: "/profile", label: "Профиль" },
    { path: "/login", label: "Вход" },
    { path: "/register", label: "Регистрация" },
  ];

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        padding: "15px 50px",
        backgroundColor: scrolled ? "#ffffffee" : "#ffffffcc",
        backdropFilter: "blur(8px)",
        boxShadow: scrolled
          ? "0 12px 35px rgba(0,0,0,0.25)"
          : "0 8px 25px rgba(0,0,0,0.2)",
        fontFamily: "'Inter', sans-serif",
        position: "sticky",
        top: 0,
        zIndex: 1000,
        transition: "all 0.3s ease",
      }}
    >
      {/* Логотип */}
      <div
        style={{
          fontWeight: 700,
          fontSize: 28,
          color: "#007bff",
          cursor: "pointer",
          transition: "transform 0.4s, color 0.4s",
        }}
        onMouseEnter={(e) => (e.currentTarget.style.transform = "rotate(-5deg) scale(1.1)")}
        onMouseLeave={(e) => (e.currentTarget.style.transform = "rotate(0deg) scale(1)")}
      >
        SafePlate
      </div>

      {/* Ссылки */}
      <div style={{ display: "flex", gap: "30px" }}>
        {links.map((link) => (
          <NavLink
            key={link.path}
            to={link.path}
            style={({ isActive }) => ({
              position: "relative",
              textDecoration: "none",
              color: isActive ? "#007bff" : "#555",
              fontWeight: 500,
              fontSize: 16,
              padding: "5px 0",
              transition: "color 0.3s, transform 0.3s, text-shadow 0.3s",
            })}
          >
            {({ isActive }) => (
              <span
                style={{
                  position: "relative",
                  paddingBottom: 2,
                  display: "inline-block",
                  cursor: "pointer",
                  transition: "transform 0.2s, text-shadow 0.2s",
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = "scale(1.08)";
                  e.currentTarget.style.textShadow = "0 2px 8px rgba(0,123,255,0.3)";
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = "scale(1)";
                  e.currentTarget.style.textShadow = "none";
                }}
              >
                {link.label}
                <span
                  style={{
                    position: "absolute",
                    bottom: 0,
                    left: 0,
                    height: 3,
                    width: "100%",
                    borderRadius: 2,
                    background: isActive
                      ? "linear-gradient(90deg, #007bff, #00c6ff)"
                      : "linear-gradient(90deg, transparent, transparent)",
                    transition: "all 0.3s",
                  }}
                />
              </span>
            )}
          </NavLink>
        ))}
      </div>
    </nav>
  );
};

export default Navbar;
