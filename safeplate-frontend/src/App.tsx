import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { PrivateRoute } from './components/PrivateRoute';
import Navbar from './components/Navbar';
import MenuPage from './pages/MenuPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfilePage from './pages/ProfilePage';
import FavoritesPage from './pages/FavoritesPage';
import AIPage from './pages/AIPage';

const App: React.FC = () => {
    return (
        <Router>
            <AuthProvider>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Navigate to="/menu" />} />
                    <Route path="/menu" element={<MenuPage />} />
                    <Route path="/login" element={<LoginPage />} />
                    <Route path="/register" element={<RegisterPage />} />
                    <Route path="/profile" element={
                        <PrivateRoute>
                            <ProfilePage />
                        </PrivateRoute>
                    } />
                    <Route path="/favorites" element={
                        <PrivateRoute>
                            <FavoritesPage />
                        </PrivateRoute>
                    } />
                    <Route path="/ai" element={
                        <PrivateRoute>
                            <AIPage />
                        </PrivateRoute>
                    } />
                </Routes>
            </AuthProvider>
        </Router>
    );
};

export default App;