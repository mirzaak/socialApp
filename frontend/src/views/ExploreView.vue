<template>
    <div class="max-w-6xl mx-auto px-4 py-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-6">Explore</h1>
      
      <!-- Loading State -->
      <div v-if="isLoading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <div v-for="i in 12" :key="i" class="aspect-square bg-gray-300 rounded-lg animate-pulse"></div>
      </div>
      
      <!-- Posts Grid -->
      <div v-else-if="explorePosts.length" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <div
          v-for="post in explorePosts"
          :key="post.id"
          @click="viewPost(post)"
          class="relative aspect-square cursor-pointer group overflow-hidden rounded-lg"
        >
          <img
            :src="`${mediaUrl}${post.image}`"
            :alt="post.caption"
            class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-110"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <div class="absolute bottom-4 left-4 text-white">
              <p class="font-semibold">@{{ post.user.username }}</p>
              <div class="flex items-center space-x-4 text-sm">
                <span class="flex items-center">
                  <HeartIcon class="h-4 w-4 mr-1" />
                  {{ post.likes_count }}
                </span>
                <span class="flex items-center">
                  <ChatBubbleOvalLeftIcon class="h-4 w-4 mr-1" />
                  {{ post.comments_count }}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <PhotoIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">No posts to explore</h3>
        <p class="text-gray-500">Check back later for new content!</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import api from '@/services/api';
  import { HeartIcon, ChatBubbleOvalLeftIcon, PhotoIcon } from '@heroicons/vue/24/solid';
  
  const router = useRouter();
  const explorePosts = ref([]);
  const isLoading = ref(true);
  const mediaUrl = process.env.VUE_APP_MEDIA_URL || 'http://localhost:8000';
  
  const fetchExplorePosts = async () => {
    try {
      // Using the feed endpoint as a fallback since explore endpoint might not exist
      const response = await api.getFeed();
      explorePosts.value = response.data.results || response.data || [];
    } catch (error) {
      console.error('Failed to fetch explore posts:', error);
      explorePosts.value = [];
    } finally {
      isLoading.value = false;
    }
  };
  
  const viewPost = (post) => {
    router.push(`/post/${post.id}`);
  };
  
  onMounted(() => {
    fetchExplorePosts();
  });
  </script>