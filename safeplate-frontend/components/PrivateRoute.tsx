import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface PrivateRouteProps {
    children: React.ReactElement;
}

export const PrivateRoute: React.FC<PrivateRouteProps> = ({ children }) => {
    const { user, loading } = useAuth();
    
    if (loading) {
        return <div style={{ textAlign: 'center', padding: '50px' }}>Загрузка...</div>;
    }
    
    return user ? children : <Navigate to="/login" />;
};
