<template>
  <div class="max-w-2xl mx-auto px-4 py-6">
    <!-- Tab Navigation -->
    <div class="flex border-b border-gray-200 mb-6">
      <button
        @click="activeTab = 'feed'"
        :class="[
          'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
          activeTab === 'feed'
            ? 'border-primary-600 text-primary-600'
            : 'border-transparent text-gray-500 hover:text-gray-700'
        ]"
      >
        Feed
      </button>
      <button
        @click="activeTab = 'my-posts'"
        :class="[
          'px-4 py-2 font-medium text-sm border-b-2 transition-colors',
          activeTab === 'my-posts'
            ? 'border-primary-600 text-primary-600'
            : 'border-transparent text-gray-500 hover:text-gray-700'
        ]"
      >
        My Posts
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && !currentPosts.length" class="space-y-4">
      <PostSkeleton v-for="i in 3" :key="i" />
    </div>

    <!-- Posts Feed -->
    <div v-else-if="currentPosts.length" class="space-y-6">
      <PostCard
        v-for="post in currentPosts"
        :key="post.pk || post.id"
        :post="post"
        :show-author="activeTab === 'feed'"
        @deleted="handlePostDeleted"
        @liked="handlePostLiked"
        @commented="handlePostCommented"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <PhotoIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">
        {{ emptyStateTitle }}
      </h3>
      <p class="text-gray-500 mb-6">{{ emptyStateMessage }}</p>
      <router-link
        v-if="activeTab === 'feed'"
        to="/explore"
        class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      >
        Explore Posts
      </router-link>
      <button
        v-else
        @click="$emit('create-post')"
        class="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
      >
        Create Your First Post
      </button>
    </div>

    <!-- Infinite Scroll Loader -->
    <div
      v-if="hasMore && !isLoading"
      ref="loadMoreTrigger"
      class="py-4 text-center"
    >
      <div class="inline-flex items-center space-x-2 text-gray-500">
        <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
        <span>Loading more posts...</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';
import { usePostsStore } from '@/stores/posts';
import PostCard from '@/components/posts/PostCard.vue';
import PostSkeleton from '@/components/posts/PostSkeleton.vue';
import { PhotoIcon } from '@heroicons/vue/24/outline';

const emit = defineEmits(['create-post']);

const postsStore = usePostsStore();
const loadMoreTrigger = ref(null);
const activeTab = ref('feed');

// Computed properties
const currentPosts = computed(() => {
  return activeTab.value === 'feed' ? postsStore.feedPosts : postsStore.myPosts;
});

const isLoading = computed(() => {
  return activeTab.value === 'feed' ? postsStore.isLoading : postsStore.isMyPostsLoading;
});

const hasMore = computed(() => {
  return activeTab.value === 'feed' ? postsStore.hasMore : postsStore.myPostsHasMore;
});

const emptyStateTitle = computed(() => {
  return activeTab.value === 'feed' ? 'No posts in your feed' : 'No posts yet';
});

const emptyStateMessage = computed(() => {
  return activeTab.value === 'feed' 
    ? 'Follow people to see their posts here'
    : 'Create your first post to get started';
});

// Methods
let observer = null;

const setupInfiniteScroll = () => {
  if (observer) {
    observer.disconnect();
  }
  
  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting && hasMore.value && !isLoading.value) {
        if (activeTab.value === 'feed') {
          postsStore.loadMoreFeedPosts();
        } else {
          postsStore.loadMoreMyPosts();
        }
      }
    },
    { threshold: 0.1 }
  );

  if (loadMoreTrigger.value) {
    observer.observe(loadMoreTrigger.value);
  }
};

const handlePostDeleted = (postId) => {
  postsStore.deletePost(postId);
};

const handlePostLiked = (postId) => {
  postsStore.toggleLike(postId);
};

const handlePostCommented = (postId, comment) => {
  postsStore.addComment(postId, comment);
};

const loadPosts = async () => {
  if (activeTab.value === 'feed') {
    await postsStore.refreshFeed();
  } else {
    await postsStore.refreshMyPosts();
  }
};

// Watchers
watch(activeTab, async (newTab) => {
  await loadPosts();
  // Re-setup infinite scroll when tab changes
  setTimeout(() => {
    setupInfiniteScroll();
  }, 100);
});

// Lifecycle hooks
onMounted(async () => {
  await loadPosts();
  setupInfiniteScroll();
});

onUnmounted(() => {
  if (observer) {
    observer.disconnect();
  }
});

// Expose methods for parent component
defineExpose({
  refreshFeed: () => postsStore.refreshFeed(),
  refreshMyPosts: () => postsStore.refreshMyPosts(),
  activeTab,
});
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>