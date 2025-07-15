import { defineStore } from 'pinia';
import api from '@/services/api';
import router from '@/router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    username: localStorage.getItem('username') || null,
    isLoading: false,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user,
  },

  actions: {
    async login(credentials) {
      this.isLoading = true;
      try {
        const response = await api.login(credentials);
        this.token = response.data.access;
        this.refreshToken = response.data.refresh;
        this.username = credentials.username; // Assuming username is part of credentials

        localStorage.setItem('access_token', this.token);
        localStorage.setItem('refresh_token', this.refreshToken);
        localStorage.setItem('username', credentials.username);

        // Update axios default header via the exposed client
        api.client.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;

        await this.fetchUser();
        return { success: true };
      } catch (error) {
        console.error('Login error:', error);
        return {
          success: false,
          error: error.response?.data?.detail || 'Invalid credentials'
        };
      } finally {
        this.isLoading = false;
      }
    },

    async fetchUser() {
      if (!this.token) return;

      try {
        const response = await api.getMyProfile();
        this.user = response.data;
        // Assuming your profile endpoint returns the user's username for consistency
        if (response.data.username) {
          localStorage.setItem('username', response.data.username);
          this.username = response.data.username;
        }
      } catch (error) {
        console.error('Failed to fetch user:', error);
        // The interceptor in api.js should handle 401 errors,
        // but it's good to have a fallback here.
        if (error.response?.status === 401) {
          this.logout();
        }
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      this.refreshToken = null;
      this.username = null;
      localStorage.clear();
      delete api.client.defaults.headers.common['Authorization']; // Clear the header
      router.push('/login');
    },

    async initializeAuth() {
      if (this.token) {
        api.client.defaults.headers.common['Authorization'] = `Bearer ${this.token}`; // Set header
        await this.fetchUser();
      }
    }
  },
});