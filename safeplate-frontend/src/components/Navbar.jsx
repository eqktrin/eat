// src/components/Navbar.jsx
import React from "react";
import { Link } from "react-router-dom";
import logo from "../assets/logo.svg"; // твой логотип

const Navbar = () => {
  return (
    <nav style={styles.navbar}>
      <div style={styles.left}>
        <img src={logo} alt="SafePlate" style={styles.logo} />
        <Link to="/menu" style={styles.link}>Меню</Link>
        <Link to="/ai" style={styles.link}>AI поиск</Link>
      </div>

      <div style={styles.right}>
        <Link to="/favorites" style={styles.link}>Избранное</Link>
        <Link to="/profile" style={styles.link}>Профиль</Link>
        <Link to="/login" style={styles.link}>Вход</Link>
      </div>
    </nav>
  );
};

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 20px",
    backgroundColor: "#ffffff",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  left: {
    display: "flex",
    alignItems: "center",
    gap: "20px",
  },
  right: {
    display: "flex",
    alignItems: "center",
    gap: "15px",
  },
  logo: {
    width: "120px",
  },
  link: {
    textDecoration: "none",
    color: "#333",
    fontWeight: "500",
  },
};

export default Navbar;
