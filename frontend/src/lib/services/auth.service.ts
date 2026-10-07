import { api } from '../api';

export interface User {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_verified: boolean;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export const authService = {
  login: async (credentials: { email: string; password: string }) => {
    const response = await api.post<AuthResponse>('/auth/login', credentials);
    return response.data;
  },
  
  register: async (data: { email: string; password: string; full_name: string }) => {
    const response = await api.post<User>('/auth/register', data);
    return response.data;
  },
  
  logout: async (refreshToken: string) => {
    await api.post('/auth/logout', { refresh_token: refreshToken });
  },
  
  getMe: async (userId: string) => {
    const response = await api.get<User>('/auth/me', { params: { user_id: userId } });
    return response.data;
  }
};
