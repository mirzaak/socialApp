<template>
  <div id="app" class="min-h-screen bg-gray-50">
    <Navbar v-if="authStore.isAuthenticated" />
    <main class="pb-16 sm:pb-0">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <MobileNav v-if="authStore.isAuthenticated && isMobile" />
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import Navbar from '@/components/layout/Navbar.vue';
import MobileNav from '@/components/layout/MobileNav.vue';

const authStore = useAuthStore();
const windowWidth = ref(window.innerWidth);

const isMobile = computed(() => windowWidth.value < 640);

onMounted(async () => {
  await authStore.initializeAuth();
  
  window.addEventListener('resize', () => {
    windowWidth.value = window.innerWidth;
  });
});
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
  font-family: 'Inter', sans-serif;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>