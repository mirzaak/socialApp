// services/api.js
import axios from 'axios';

// Create axios instance
const client = axios.create({
  baseURL: '/app',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type'];
    }
    
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
client.interceptors.response.use(
  response => response,
  async (error) => {
    if (error.config?.url === '/auth/register/') {
      console.error('Registration error:', error.response?.data);
    }
    
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      const refreshToken = localStorage.getItem('refresh_token');
      
      if (refreshToken) {
        try {
          const res = await client.post('/auth/refresh/', { refresh: refreshToken });
          localStorage.setItem('access_token', res.data.access);
          originalRequest.headers.Authorization = `Bearer ${res.data.access}`;
          return client(originalRequest);
        } catch (refreshError) {
          localStorage.clear();
          window.location.href = '/login';
        }
      } else {
        localStorage.clear();
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// API methods
const api = {
  // Export the client explicitly
  client: client,

  // Authentication
  login: (credentials) => client.post('/auth/login/', credentials),
  register: (userData) => client.post('/auth/register/', userData),
  refreshToken: (refresh) => client.post('/auth/refresh/', { refresh }),

  // Profile
  getMyProfile: () => client.get('/profile/'),
  getUserProfile: (username) => client.get(`/profile/${username}/`),
  followUser: (username) => client.post(`/profile/${username}/follow/`),

  // Posts
  getPosts: (page = 1) => client.get('/posts/', { params: { page } }),
  createPost: (postData) => client.post('/posts/', postData),
  getPostDetail: (pk) => client.get(`/posts/${pk}/`),
  likePost: (postId) => client.post(`/posts/${postId}/like/`),
  commentOnPost: (postId, text) => client.post(`/posts/${postId}/comment/`, { text }),
  getUserPosts: (username) => client.get(`/posts/user/${username}/`),
  getMyPosts: (page = 1) => client.get('/posts/my/', { params: { page } }),

  // Search & Explore
  explorePosts: () => client.get('/explore/'),
  searchUsers: (query) => client.get('/search/', { params: { search: query } }),
};

export default api;