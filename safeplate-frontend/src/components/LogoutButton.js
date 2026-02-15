// safeplate-frontend/src/components/LogoutButton.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_email");
    alert("Вы вышли из системы");
    navigate("/login");
  };

  return (
    <button onClick={handleLogout} style={{ padding: '8px 16px', margin: '10px' }}>
      Выйти
    </button>
  );
};

export default LogoutButton;