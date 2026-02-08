'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { AuthState, User, UserLogin, UserRegister } from '../types';
import { apiClient } from '../lib/api-client';

interface AuthContextType {
  authState: AuthState;
  login: (credentials: UserLogin) => Promise<void>;
  register: (userData: UserRegister) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    token: null,
  });

  useEffect(() => {
    // Check if token exists and is valid on initial load (client-side only)
    const token = localStorage.getItem('token');
    if (token) {
      setAuthState({
        user: null,
        isAuthenticated: true,
        token,
      });
    }
  }, []);

  const login = async (credentials: UserLogin) => {
    try {
      const response = await apiClient.signIn(credentials);

      if (response.access_token) {
        const { access_token, user } = response;

        localStorage.setItem('token', access_token);

        setAuthState({
          user,
          isAuthenticated: true,
          token: access_token,
        });
      } else {
        throw new Error('Login failed: No token received');
      }
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    }
  };

  const register = async (userData: UserRegister) => {
    try {
      const response = await apiClient.signUp(userData);

      if (response.user && response.access_token) {
        const { access_token, user } = response;

        localStorage.setItem('token', access_token);

        setAuthState({
          user,
          isAuthenticated: true,
          token: access_token,
        });
      } else {
        throw new Error('Registration failed: No token received');
      }
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');

    setAuthState({
      user: null,
      isAuthenticated: false,
      token: null,
    });
  };

  const value: AuthContextType = {
    authState,
    login,
    register,
    logout,
    isAuthenticated: !!authState.token,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};