import React, { createContext, useState, useEffect, useContext } from 'react';
import axios from 'axios';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkUser = async () => {
            const token = localStorage.getItem('token');
            if (token) {
                axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                try {
                    const res = await axios.get('http://127.0.0.1:8000/api/v1/auth/me');
                    setUser({ token, ...res.data });
                } catch (err) {
                    console.error("Sessão inválida:", err);
                    logout(); // Token expirado ou inválido
                }
            }
            setLoading(false);
        };
        checkUser();
    }, []);

    const login = async (email, password) => {
        try {
            const response = await axios.post('http://127.0.0.1:8000/api/v1/auth/login', {
                username: email, // FastAPI OAuth2PasswordRequestForm expects 'username'
                password: password
            }, {
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
            });

            const { access_token } = response.data;
            localStorage.setItem('token', access_token);
            axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
            setUser({ token: access_token, email });
            return true;
        } catch (error) {
            console.error("Login failed:", error);
            throw error;
        }
    };

    const signup = async (email, password, empresa) => {
        try {
            await axios.post('http://127.0.0.1:8000/api/v1/auth/signup', {
                email,
                password,
                nome_empresa: empresa
            });
            return true;
        } catch (error) {
            console.error("Signup failed:", error);
            throw error;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        delete axios.defaults.headers.common['Authorization'];
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, signup, logout, loading }}>
            {!loading && children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
