import React from "react";
import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";

// Страницы
import MenuPage from "./pages/MenuPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import ProfilePage from "./pages/ProfilePage";
import FavoritesPage from "./pages/FavoritesPage";
import AIPage from "./pages/AIPage";

const App = () => {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Navigate to="/menu" />} />
        <Route path="/menu" element={<MenuPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/favorites" element={<FavoritesPage />} />
        <Route path="/ai" element={<AIPage />} />
      </Routes>
    </Router>
  );
};

export default App;