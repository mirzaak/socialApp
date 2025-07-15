<template>
    <div class="max-w-4xl mx-auto px-4 py-6">
      <div class="mb-6">
        <input
          v-model="searchQuery"
          @input="handleSearch"
          type="text"
          placeholder="Search users..."
          class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          autofocus
        />
      </div>
  
      <!-- Loading State -->
      <div v-if="isLoading" class="space-y-4">
        <div v-for="i in 5" :key="i" class="flex items-center space-x-4 p-4 bg-white rounded-lg animate-pulse">
          <div class="h-12 w-12 bg-gray-300 rounded-full"></div>
          <div class="flex-1">
            <div class="h-4 bg-gray-300 rounded w-1/4 mb-2"></div>
            <div class="h-3 bg-gray-200 rounded w-1/3"></div>
          </div>
        </div>
      </div>
  
      <!-- Search Results -->
      <div v-else-if="searchResults.length" class="space-y-2">
        <router-link
          v-for="user in searchResults"
          :key="user.id"
          :to="`/profile/${user.user.username}`"
          class="flex items-center space-x-4 p-4 bg-white rounded-lg hover:bg-gray-50 transition-colors"
        >
          <img
            :src="user.image ? `${mediaUrl}${user.image}` : '/default-avatar.png'"
            :alt="user.user.username"
            class="h-12 w-12 rounded-full object-cover"
          />
          <div class="flex-1">
            <p class="font-semibold text-gray-900">{{ user.user.username }}</p>
            <p class="text-sm text-gray-500">{{ user.bio || 'No bio' }}</p>
          </div>
        </router-link>
      </div>
  
      <!-- Empty State -->
      <div v-else-if="hasSearched" class="text-center py-12">
        <MagnifyingGlassIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">No users found</h3>
        <p class="text-gray-500">Try searching with a different term</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute } from 'vue-router';
  import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline';
  import api from '@/services/api';
  
  const route = useRoute();
  const searchQuery = ref('');
  const searchResults = ref([]);
  const isLoading = ref(false);
  const hasSearched = ref(false);
  const mediaUrl = process.env.VUE_APP_MEDIA_URL || 'http://localhost:8000';
  
  let searchTimeout = null;
  
  const handleSearch = () => {
    clearTimeout(searchTimeout);
    
    if (!searchQuery.value.trim()) {
      searchResults.value = [];
      hasSearched.value = false;
      return;
    }
    
    searchTimeout = setTimeout(async () => {
      isLoading.value = true;
      hasSearched.value = true;
      
      try {
        const response = await api.searchUsers(searchQuery.value);
        searchResults.value = response.data.results || response.data || [];
      } catch (error) {
        console.error('Search failed:', error);
        searchResults.value = [];
      } finally {
        isLoading.value = false;
      }
    }, 300);
  };
  
  onMounted(() => {
    if (route.query.q) {
      searchQuery.value = route.query.q;
      handleSearch();
    }
  });
  </script>