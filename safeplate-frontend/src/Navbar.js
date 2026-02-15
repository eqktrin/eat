import React from "react";
import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav style={{ padding: "10px", backgroundColor: "#eee" }}>
      <Link to="/menu" style={{ marginRight: "10px" }}>Меню</Link>
      <Link to="/favorites" style={{ marginRight: "10px" }}>Избранное</Link>
      <Link to="/profile">Профиль</Link>
      <Link to="/ai">AI поиск</Link>
    </nav>
  );
};

export default Navbar;
