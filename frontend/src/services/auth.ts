// frontend/src/services/auth.ts
import { storeToken, removeToken, setAuthStatus, getToken } from '@/lib/auth';
import apiClient from './api';

interface User {
  id: string;
  name: string;
  email: string;
  created_at: string;
  updated_at: string;
}

interface SignupData {
  name: string;
  email: string;
  password: string;
}

interface LoginData {
  email: string;
  password: string;
}

/**
 * Get current user profile using the stored token
 */
export const getCurrentUser = async (): Promise<User> => {
  try {
    const response = await apiClient.get('user/');
    return response.data;
  } catch (error: any) {
    console.error('Get user profile error:', error);
    throw new Error(error.response?.data?.detail || 'Failed to fetch user profile');
  }
};

/**
 * Signup a new user
 */
export const signup = async (signupData: SignupData): Promise<{ user: User, token: string }> => {
  try {
    const response = await apiClient.post('auth/signup', signupData);
    const data = response.data;

    storeToken(data.token);
    const userProfile = await getCurrentUser();

    return {
      user: userProfile,
      token: data.token
    };
  } catch (error: any) {
    console.error('Signup error:', error);
    throw new Error(error.response?.data?.detail || 'Signup failed');
  }
};

/**
 * Login an existing user
 */
export const login = async (loginData: LoginData): Promise<{ user: User, token: string }> => {
  try {
    const response = await apiClient.post('auth/login', loginData);
    const data = response.data;

    storeToken(data.token);
    const userProfile = await getCurrentUser();

    return {
      user: userProfile,
      token: data.token
    };
  } catch (error: any) {
    console.error('Login error:', error);
    throw new Error(error.response?.data?.detail || 'Login failed');
  }
};

/**
 * Logout the current user
 */
export const logout = async (): Promise<void> => {
  try {
    removeToken();
    setAuthStatus(false);
  } catch (error) {
    console.error('Logout error:', error);
    throw error;
  }
};