<template>
  <nav class="bg-white border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center">
          <div class="text-2xl font-bold bg-gradient-to-r from-primary-500 to-primary-600 bg-clip-text text-transparent">
            SocialApp
          </div>
        </router-link>

        <!-- Search Bar (Desktop) -->
        <div class="hidden sm:block flex-1 max-w-md mx-8">
          <div class="relative">
            <input
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              type="text"
              placeholder="Search users..."
              class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
            <MagnifyingGlassIcon class="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
          </div>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden sm:flex items-center space-x-4">
          <router-link
            to="/"
            class="p-2 text-gray-600 hover:text-primary-600 transition-colors"
          >
            <HomeIcon class="h-6 w-6" />
          </router-link>
          
          <router-link
            to="/explore"
            class="p-2 text-gray-600 hover:text-primary-600 transition-colors"
          >
            <MagnifyingGlassCircleIcon class="h-6 w-6" />
          </router-link>
          
          <button
            @click="showCreatePost = true"
            class="p-2 text-gray-600 hover:text-primary-600 transition-colors"
          >
            <PlusCircleIcon class="h-6 w-6" />
          </button>
          
          <router-link
            to="/profile"
            class="relative"
          >
            <img
              :src="userAvatar"
              alt="Profile"
              class="h-8 w-8 rounded-full object-cover ring-2 ring-gray-200"
              @error="handleAvatarError"
            />
          </router-link>
          
          <button
            @click="logout"
            class="p-2 text-gray-600 hover:text-red-600 transition-colors"
          >
            <ArrowRightOnRectangleIcon class="h-6 w-6" />
          </button>
        </div>

        <!-- Mobile menu button -->
        <button
          @click="showMobileMenu = !showMobileMenu"
          class="sm:hidden p-2 text-gray-600"
        >
          <Bars3Icon class="h-6 w-6" />
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <transition name="slide-down">
      <div v-if="showMobileMenu" class="sm:hidden bg-white border-t border-gray-200">
        <div class="px-4 py-2">
          <input
            v-model="searchQuery"
            @keyup.enter="handleSearch"
            type="text"
            placeholder="Search users..."
            class="w-full px-4 py-2 border border-gray-300 rounded-full focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>
    </transition>

    <!-- Create Post Modal -->
    <CreatePostModal 
      :show="showCreatePost" 
      @close="showCreatePost = false"
      @posted="handlePostCreated"
    />
  </nav>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import {
  HomeIcon,
  MagnifyingGlassIcon,
  MagnifyingGlassCircleIcon,
  PlusCircleIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon
} from '@heroicons/vue/24/outline';
import CreatePostModal from '@/components/posts/CreatePostModal.vue';

const router = useRouter();
const authStore = useAuthStore();

const searchQuery = ref('');
const showMobileMenu = ref(false);
const showCreatePost = ref(false);

const userAvatar = computed(() => {
  // Check if user has a profile image
  if (authStore.user?.profile?.image) {
    if (authStore.user.profile.image.startsWith('http')) {
      return authStore.user.profile.image;
    }
    // Use proxy path - Django returns /media/profiles/image.jpg
    return authStore.user.profile.image;
  }
  
  // Check if user object has direct image property
  if (authStore.user?.image) {
    if (authStore.user.image.startsWith('http')) {
      return authStore.user.image;
    }
    // Use proxy path
    return authStore.user.image;
  }
  
  // Fallback to generated avatar with user's username
  const username = authStore.user?.username || authStore.username || 'User';
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(username)}&background=e5e7eb&color=6b7280&size=32`;
});

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push(`/search?q=${encodeURIComponent(searchQuery.value)}`);
    searchQuery.value = '';
    showMobileMenu.value = false;
  }
};

const handlePostCreated = () => {
  showCreatePost.value = false;
  router.push('/');
};

const handleAvatarError = (event) => {
  // Fallback to a different avatar service if the first one fails
  const username = authStore.user?.username || authStore.username || 'User';
  event.target.src = `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(username)}`;
};

const logout = () => {
  authStore.logout();
};
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
</style>