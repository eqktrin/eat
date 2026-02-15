import React, { createContext, useState, useEffect } from 'react';
import { api } from '../api/api';

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async () => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                const response = await api.get('/profile');
                setUser(response.data);
            } catch (error) {
                localStorage.removeItem('token');
            }
        }
        setLoading(false);
    };

    const updateUserAllergens = (allergens) => {
        setUser(prev => ({
            ...prev,
            allergens: allergens
        }));
    };

    return (
        <AuthContext.Provider value={{ 
            user, 
            setUser, 
            loading, 
            updateUserAllergens 
        }}>
            {children}
        </AuthContext.Provider>
    );
};