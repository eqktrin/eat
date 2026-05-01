// safeplate-frontend/src/components/LogoutButton.tsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

const LogoutButton: React.FC = () => {
  const navigate = useNavigate();

  const handleLogout = (): void => {
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