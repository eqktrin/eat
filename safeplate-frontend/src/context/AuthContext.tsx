import React, { createContext, useState, useEffect, ReactNode } from 'react';
import api from '../api/api';

interface User {
    id: number;
    email: string;
    role: string;
    allergens?: string[];
}

interface AuthContextType {
    user: User | null;
    loading: boolean;
    login: (email: string, password: string) => Promise<void>;
    logout: () => void;
    updateUserAllergens: (allergens: string[]) => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
    children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState<boolean>(true);

    useEffect(() => {
        checkAuth();
    }, []);

    const checkAuth = async (): Promise<void> => {
        const token = localStorage.getItem('access_token');
        if (!token) {
            setLoading(false);
            return;
        }
        try {
            const response = await api.get<User>('/profile/me');
            setUser(response.data);
        } catch (error) {
            localStorage.removeItem('access_token');
        } finally {
            setLoading(false);
        }
    };

    const login = async (email: string, password: string): Promise<void> => {
        // ИСПРАВЛЕНО: используем URLSearchParams вместо FormData
        const params = new URLSearchParams();
        params.append('username', email);
        params.append('password', password);

        const response = await api.post<{ access_token: string }>(
            '/auth/token', 
            params.toString(),
            {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            }
        );
        
        localStorage.setItem('access_token', response.data.access_token);
        
        const userResponse = await api.get<User>('/profile/me');
        setUser(userResponse.data);
    };

    const logout = (): void => {
        localStorage.removeItem('access_token');
        setUser(null);
    };

    const updateUserAllergens = (allergens: string[]): void => {
        setUser(prev => prev ? { ...prev, allergens } : prev);
    };

    return (
        <AuthContext.Provider value={{ user, loading, login, logout, updateUserAllergens }}>
            {children}
        </AuthContext.Provider>
    );
};