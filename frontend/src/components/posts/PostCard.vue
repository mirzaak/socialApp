<template>
  <article class="bg-white rounded-lg shadow-sm overflow-hidden">
    <!-- Post Header -->
    <div class="flex items-center justify-between p-4">
      <router-link 
        :to="`/profile/${post.user}`"
        class="flex items-center space-x-3 group"
      >
        <img
          :src="userAvatar"
          :alt="post.user"
          class="h-10 w-10 rounded-full object-cover ring-2 ring-gray-100"
          @error="handleAvatarError"
        />
        <div>
          <p class="font-semibold text-gray-900 group-hover:text-primary-600 transition-colors">
            {{ post.user }}
          </p>
        </div>
      </router-link>
      
      <button
        v-if="isOwnPost"
        @click="showMenu = !showMenu"
        class="p-2 text-gray-400 hover:text-gray-600 relative"
      >
        <EllipsisHorizontalIcon class="h-5 w-5" />
      </button>
    </div>

    <!-- Post Image -->
    <div v-if="postImage" class="relative aspect-square bg-gray-100">
      <img
        :src="postImage"
        :alt="post.caption"
        class="w-full h-full object-cover"
        @dblclick="handleLike"
        @error="handleImageError"
      />
    </div>

    <!-- Post Actions -->
    <div class="p-4">
      <div class="flex items-center space-x-4 mb-3">
        <button
          @click="handleLike"
          class="flex items-center space-x-1 group"
        >
          <HeartIcon
            class="h-6 w-6 transition-all"
            :class="isLiked ? 'text-red-500 fill-current' : 'text-gray-700'"
          />
        </button>
        
        <button
          @click="focusComment"
          class="flex items-center space-x-1 group"
        >
          <ChatBubbleOvalLeftIcon class="h-6 w-6 text-gray-700" />
        </button>
      </div>

      <!-- Likes Count -->
      <p class="font-semibold text-sm text-gray-900 mb-2">
        {{ post.likes?.length || 0 }} {{ post.likes?.length === 1 ? 'like' : 'likes' }}
      </p>

      <!-- Caption -->
      <div class="mb-3">
        <span class="font-semibold text-sm">{{ post.user }}</span>
        <span class="text-sm text-gray-700 ml-2">{{ post.caption }}</span>
      </div>

      <!-- Comments -->
      <div v-if="post.comments?.length > 0" class="mb-3 space-y-1">
        <div
          v-for="comment in post.comments.slice(-3)"
          :key="comment.pk"
          class="text-sm"
        >
          <span class="font-semibold">{{ comment.user }}</span>
          <span class="ml-2 text-gray-700">{{ comment.text }}</span>
        </div>
      </div>

      <!-- Add Comment -->
      <form @submit.prevent="handleComment" class="flex items-center space-x-2">
        <input
          ref="commentInput"
          v-model="newComment"
          type="text"
          placeholder="Add a comment..."
          class="flex-1 text-sm bg-transparent outline-none"
        />
        <button
          v-if="newComment.trim()"
          type="submit"
          class="text-sm font-semibold text-primary-600 hover:text-primary-700"
        >
          Post
        </button>
      </form>
    </div>
  </article>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { usePostsStore } from '@/stores/posts';
import {
  HeartIcon,
  ChatBubbleOvalLeftIcon,
  EllipsisHorizontalIcon
} from '@heroicons/vue/24/outline';
import { HeartIcon as HeartIconSolid } from '@heroicons/vue/24/solid';

const props = defineProps({
  post: {
    type: Object,
    required: true
  }
});

const authStore = useAuthStore();
const postsStore = usePostsStore();

const showMenu = ref(false);
const newComment = ref('');
const commentInput = ref(null);

const isOwnPost = computed(() => 
  authStore.username === props.post.user
);

const isLiked = computed(() => {
  const userId = parseInt(localStorage.getItem('user_id'));
  return props.post.likes?.includes(userId) || false;
});

const userAvatar = computed(() => {
  const mediaUrl = 'http://localhost:8000';
  if (props.post.profilefull?.image) {
    // Check if it already has the full URL
    if (props.post.profilefull.image.startsWith('http')) {
      return props.post.profilefull.image;
    }
    return `${mediaUrl}${props.post.profilefull.image}`;
  }
  // Use a reliable online avatar service as fallback
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(props.post.user)}&background=e5e7eb&color=6b7280&size=40`;
});

const postImage = computed(() => {
  const mediaUrl = 'http://localhost:8000';
  if (props.post.image) {
    // Check if it already has the full URL
    if (props.post.image.startsWith('http')) {
      return props.post.image;
    }
    return `${mediaUrl}${props.post.image}`;
  }
  return null; // Handle posts without images
});

const handleLike = async () => {
  await postsStore.toggleLike(props.post.pk);
};

const handleComment = async () => {
  if (newComment.value.trim()) {
    await postsStore.addComment(props.post.pk, newComment.value);
    newComment.value = '';
  }
};

const focusComment = () => {
  commentInput.value?.focus();
};

const handleAvatarError = (event) => {
  // Fallback to a different avatar service if the first one fails
  event.target.src = `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(props.post.user)}`;
};

const handleImageError = (event) => {
  console.error('Failed to load image:', event.target.src);
  event.target.style.display = 'none';
};
</script>