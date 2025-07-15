<template>
    <div class="max-w-4xl mx-auto px-4 py-6">
      <div v-if="post" class="bg-white rounded-lg shadow-sm overflow-hidden">
        <PostCard :post="post" @deleted="handleDeleted" />
      </div>
      <div v-else class="text-center py-12">
        <p class="text-gray-500">Loading post...</p>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import PostCard from '@/components/posts/PostCard.vue';
  import api from '@/services/api';
  
  const route = useRoute();
  const router = useRouter();
  const post = ref(null);
  
  const fetchPost = async () => {
    try {
      // Since we don't have a single post endpoint, we'll need to fetch from feed
      // In a real app, you'd have a dedicated endpoint
      const response = await api.getFeed();
      const posts = response.data.results || response.data || [];
      post.value = posts.find(p => p.id === parseInt(route.params.id));
    } catch (error) {
      console.error('Failed to fetch post:', error);
    }
  };
  
  const handleDeleted = () => {
    router.push('/');
  };
  
  onMounted(() => {
    fetchPost();
  });
  </script>