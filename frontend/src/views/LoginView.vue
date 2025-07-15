<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4">
      <div class="max-w-md w-full">
        <div class="text-center mb-8">
          <h1 class="text-4xl font-bold bg-gradient-to-r from-primary-500 to-primary-600 bg-clip-text text-transparent">
            SocialApp
          </h1>
          <p class="text-gray-600 mt-2">Welcome back!</p>
        </div>
  
        <div class="bg-white rounded-2xl shadow-xl p-8">
          <form @submit.prevent="handleLogin" class="space-y-6">
            <div>
              <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
                Username
              </label>
              <input
                id="username"
                v-model="form.username"
                type="text"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Enter your username"
              />
            </div>
  
            <div>
              <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                id="password"
                v-model="form.password"
                type="password"
                required
                class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                placeholder="Enter your password"
              />
            </div>
  
            <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-lg">
              <p class="text-sm text-red-600">{{ error }}</p>
            </div>
  
            <button
              type="submit"
              :disabled="isLoading"
              class="w-full py-3 px-4 bg-gradient-to-r from-primary-600 to-primary-700 text-white font-semibold rounded-lg hover:from-primary-700 hover:to-primary-800 focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
            >
              {{ isLoading ? 'Signing in...' : 'Sign In' }}
            </button>
          </form>
  
          <p class="text-center text-sm text-gray-600 mt-6">
            Don't have an account?
            <router-link to="/register" class="font-medium text-primary-600 hover:text-primary-500">
              Sign up
            </router-link>
          </p>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { useRouter } from 'vue-router';
  import { useAuthStore } from '@/stores/auth';
  
  const router = useRouter();
  const authStore = useAuthStore();
  
  const form = ref({
    username: '',
    password: ''
  });
  
  const isLoading = ref(false);
  const error = ref('');
  
  const handleLogin = async () => {
    error.value = '';
    isLoading.value = true;
  
    const result = await authStore.login(form.value);
  
    if (result.success) {
      router.push('/');
    } else {
      error.value = result.error;
    }}
    </script>