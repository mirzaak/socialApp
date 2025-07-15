<template>
  <div class="max-w-4xl mx-auto px-4 py-6">
    <!-- Profile Header -->
    <div class="bg-white rounded-lg shadow-sm p-6 mb-6">
      <div class="flex flex-col sm:flex-row items-center sm:items-start space-y-4 sm:space-y-0 sm:space-x-6">
        <!-- Avatar -->
        <div class="relative">
          <img
            :src="profileAvatar"
            :alt="profile?.user?.username"
            class="h-32 w-32 rounded-full object-cover ring-4 ring-gray-100"
            @error="handleAvatarError"
          />
          <button
            v-if="isOwnProfile"
            @click="$refs.avatarInput.click()"
            class="absolute bottom-0 right-0 p-2 bg-primary-600 text-white rounded-full hover:bg-primary-700 transition-colors"
          >
            <CameraIcon class="h-5 w-5" />
          </button>
          <input
            ref="avatarInput"
            type="file"
            accept="image/*"
            @change="handleAvatarChange"
            class="hidden"
          />
        </div>

        <!-- Profile Info -->
        <div class="flex-1 text-center sm:text-left">
          <div class="flex flex-col sm:flex-row items-center sm:items-start space-y-3 sm:space-y-0 sm:space-x-4">
            <h1 class="text-2xl font-bold text-gray-900">
              {{ profile?.user?.username }}
            </h1>
            <div v-if="!isOwnProfile" class="flex space-x-2">
              <button
                @click="toggleFollow"
                class="px-6 py-2 rounded-lg font-medium transition-colors"
                :class="isFollowing 
                  ? 'bg-gray-200 text-gray-700 hover:bg-gray-300' 
                  : 'bg-primary-600 text-white hover:bg-primary-700'"
              >
                {{ isFollowing ? 'Following' : 'Follow' }}
              </button>
              <button class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors">
                Message
              </button>
            </div>
            <button
              v-else
              @click="showEditProfile = true"
              class="px-6 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
            >
              Edit Profile
            </button>
          </div>

          <!-- Stats -->
          <div class="flex justify-center sm:justify-start space-x-8 mt-6">
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-900">{{ userPosts.length }}</p>
              <p class="text-sm text-gray-500">Posts</p>
            </div>
            <button class="text-center group">
              <p class="text-2xl font-bold text-gray-900">{{ profile?.followers_count || 0 }}</p>
              <p class="text-sm text-gray-500 group-hover:text-gray-700">Followers</p>
            </button>
            <button class="text-center group">
              <p class="text-2xl font-bold text-gray-900">{{ profile?.following_count || 0 }}</p>
              <p class="text-sm text-gray-500 group-hover:text-gray-700">Following</p>
            </button>
          </div>

          <!-- Bio -->
          <div v-if="profile?.bio" class="mt-4">
            <p class="text-gray-700">{{ profile.bio }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Posts Grid -->
    <div class="grid grid-cols-3 gap-1 sm:gap-4">
      <div
        v-for="post in userPosts"
        :key="post.pk"
        @click="selectedPost = post"
        class="relative aspect-square cursor-pointer group"
      >
        <img
          v-if="post.image"
          :src="getPostImage(post)"
          :alt="post.caption"
          class="w-full h-full object-cover rounded-lg"
          @error="handlePostImageError"
        />
        <div v-else class="w-full h-full bg-gray-200 rounded-lg flex items-center justify-center">
          <span class="text-gray-500 text-sm">No Image</span>
        </div>
        <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all duration-300 rounded-lg flex items-center justify-center">
          <div class="opacity-0 group-hover:opacity-100 transition-opacity duration-300 text-white flex items-center space-x-4">
            <div class="flex items-center space-x-1">
              <HeartIcon class="h-6 w-6 fill-current" />
              <span class="font-semibold">{{ post.likes_count || 0 }}</span>
            </div>
            <div class="flex items-center space-x-1">
              <ChatBubbleOvalLeftIcon class="h-6 w-6 fill-current" />
              <span class="font-semibold">{{ post.comments_count || 0 }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="!userPosts.length && !isLoading" class="text-center py-12">
      <CameraIcon class="h-16 w-16 text-gray-400 mx-auto mb-4" />
      <h3 class="text-lg font-medium text-gray-900 mb-2">No posts yet</h3>
      <p v-if="isOwnProfile" class="text-gray-500">
        Share your first photo to get started!
      </p>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center py-8">
      <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-500"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useProfileStore } from '@/stores/profile';
import { usePostsStore } from '@/stores/posts';
import { 
  CameraIcon, 
  HeartIcon, 
  ChatBubbleOvalLeftIcon 
} from '@heroicons/vue/24/solid';
import { useToast } from 'vue-toastification';

const route = useRoute();
const authStore = useAuthStore();
const profileStore = useProfileStore();
const postsStore = usePostsStore();
const toast = useToast();

const profile = ref(null);
const userPosts = ref([]);
const selectedPost = ref(null);
const showEditProfile = ref(false);
const isLoading = ref(true);

const username = computed(() => 
  route.params.username || authStore.user?.user?.username || authStore.username
);

const isOwnProfile = computed(() => {
  const currentUsername = authStore.user?.user?.username || authStore.username;
  const profileUsername = profile.value?.user?.username;
  return currentUsername === profileUsername;
});

const isFollowing = computed(() => profile.value?.is_following || false);

const profileAvatar = computed(() => {
  // Check if profile has image
  if (profile.value?.image) {
    if (profile.value.image.startsWith('http')) {
      return profile.value.image;
    }
    // Use proxy path - Django returns /media/profiles/image.jpg
    return profile.value.image;
  }
  
  // Fallback to generated avatar
  const displayUsername = profile.value?.user?.username || username.value || 'User';
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(displayUsername)}&background=e5e7eb&color=6b7280&size=128`;
});

const getPostImage = (post) => {
  if (post.image) {
    if (post.image.startsWith('http')) {
      return post.image;
    }
    // Use proxy path - Django returns /media/posts/image.jpg
    return post.image;
  }
  return null;
};

const handleAvatarError = (event) => {
  // Fallback to different avatar service
  const displayUsername = profile.value?.user?.username || username.value || 'User';
  event.target.src = `https://api.dicebear.com/7.x/initials/svg?seed=${encodeURIComponent(displayUsername)}`;
};

const handlePostImageError = (event) => {
  event.target.style.display = 'none';
};

const fetchProfile = async () => {
  isLoading.value = true;
  try {
    const result = await profileStore.fetchProfile(username.value);
    if (result.success) {
      profile.value = result.data;
    } else {
      console.error('Failed to fetch profile:', result.error);
    }
  } catch (error) {
    console.error('Error fetching profile:', error);
  } finally {
    isLoading.value = false;
  }
};

const fetchUserPosts = async () => {
  try {
    const result = await postsStore.fetchUserPosts(username.value);
    if (result.success) {
      userPosts.value = result.data;
    }
  } catch (error) {
    console.error('Error fetching user posts:', error);
  }
};

const toggleFollow = async () => {
  try {
    const result = await profileStore.toggleFollow(username.value);
    if (result.success) {
      profile.value.is_following = result.following;
      profile.value.followers_count = result.followers_count;
    }
  } catch (error) {
    console.error('Error toggling follow:', error);
  }
};

const handleAvatarChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  if (file.size > 5 * 1024 * 1024) {
    toast.error('Image size must be less than 5MB');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  try {
    const result = await profileStore.updateProfile(formData);
    if (result.success) {
      profile.value = result.data;
      authStore.user = result.data;
      toast.success('Profile picture updated!');
    }
  } catch (error) {
    console.error('Error updating avatar:', error);
    toast.error('Failed to update profile picture');
  }
};

watch(() => route.params.username, async (newUsername) => {
  if (newUsername || route.name === 'profile') {
    await fetchProfile();
    await fetchUserPosts();
  }
});

onMounted(async () => {
  await fetchProfile();
  await fetchUserPosts();
});
</script>