
<template>
    <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-40 sm:hidden">
      <div class="flex justify-around items-center h-16">
        <router-link
          to="/"
          class="flex flex-col items-center justify-center p-2"
          :class="currentRoute === '/' ? 'text-primary-600' : 'text-gray-600'"
        >
          <HomeIcon class="h-6 w-6" />
        </router-link>
        
        <router-link
          to="/explore"
          class="flex flex-col items-center justify-center p-2"
          :class="currentRoute === '/explore' ? 'text-primary-600' : 'text-gray-600'"
        >
          <MagnifyingGlassIcon class="h-6 w-6" />
        </router-link>
        
        <button
          @click="$emit('create-post')"
          class="flex flex-col items-center justify-center p-2 text-gray-600"
        >
          <PlusCircleIcon class="h-6 w-6" />
        </button>
        
        <router-link
          to="/profile"
          class="flex flex-col items-center justify-center p-2"
          :class="currentRoute === '/profile' ? 'text-primary-600' : 'text-gray-600'"
        >
          <UserCircleIcon class="h-6 w-6" />
        </router-link>
      </div>
    </nav>
  </template>
  
  <script setup>
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';
  import {
    HomeIcon,
    MagnifyingGlassIcon,
    PlusCircleIcon,
    UserCircleIcon
  } from '@heroicons/vue/24/outline';
  
  const route = useRoute();
  const currentRoute = computed(() => route.path);
  </script>