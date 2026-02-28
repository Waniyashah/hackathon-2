import axios, { AxiosInstance } from 'axios';
import { UserLogin, UserRegister, Task, TaskCreate, TaskUpdate } from '../types';

class ApiClient {
  private client: AxiosInstance;
  private baseUrl: string;

  constructor(baseURL: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') {
    this.baseUrl = baseURL;
    this.client = axios.create({
      baseURL: this.baseUrl,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include token
    this.client.interceptors.request.use(
      (config) => {
        console.log(`Making request to: ${config.baseURL}${config.url}`);
        const token = localStorage.getItem('token');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle common errors
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      (error) => {
        if (error.response?.status === 401) {
          // Token expired or invalid, redirect to login
          localStorage.removeItem('token');
          window.location.href = '/auth/signin';
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication methods
  async signUp(userData: UserRegister) {
    try {
      const response = await this.client.post('/api/auth/signup', userData);
      return response.data;
    } catch (error: any) {
      console.error('Signup error details:', error.response?.data);
      throw error;
    }
  }

  async signIn(credentials: UserLogin) {
    const response = await this.client.post('/api/auth/signin', credentials);
    return response.data;
  }

  async signOut() {
    // JWT is stateless, so no server-side logout is needed
    // We just remove the token from local storage
    localStorage.removeItem('token');
    return { message: 'Signed out successfully' };
  }

  // Task methods
  async getTasks(userId: string) {
    const response = await this.client.get(`/api/users/${userId}/tasks`);
    return response.data;
  }

  async createTask(userId: string, taskData: TaskCreate) {
    const response = await this.client.post(`/api/users/${userId}/tasks`, taskData);
    return response.data;
  }

  async getTask(userId: string, taskId: string) {
    const response = await this.client.get(`/api/users/${userId}/tasks/${taskId}`);
    return response.data;
  }

  async updateTask(userId: string, taskId: string, taskData: TaskUpdate) {
    const response = await this.client.put(`/api/users/${userId}/tasks/${taskId}`, taskData);
    return response.data;
  }

  async deleteTask(userId: string, taskId: string) {
    const response = await this.client.delete(`/api/users/${userId}/tasks/${taskId}`);
    return response.data;
  }

  async toggleTaskCompletion(userId: string, taskId: string, completed: boolean) {
    const response = await this.client.patch(`/api/users/${userId}/tasks/${taskId}/complete`, { completed });
    return response.data;
  }
}

export const apiClient = new ApiClient();

export default ApiClient;