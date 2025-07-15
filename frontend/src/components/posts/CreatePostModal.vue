<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white rounded-lg p-6 w-full max-w-md mx-4">
      <div class="flex justify-between items-center mb-4">
        <h2 class="text-xl font-semibold">Create New Post</h2>
        <button @click="close" class="text-gray-500 hover:text-gray-700">
          <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
      </div>
      
      <form @submit.prevent="handleSubmit">
        <div class="mb-4">
          <textarea
            v-model="caption"
            placeholder="What's on your mind?"
            class="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows="4"
          ></textarea>
        </div>
        
        <div class="mb-4">
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            @change="handleFileSelect"
            class="hidden"
          />
          <button
            type="button"
            @click="$refs.fileInput.click()"
            class="flex items-center space-x-2 text-gray-600 hover:text-blue-600"
          >
            <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
            <span>Add Photo</span>
          </button>
        </div>
        
        <div v-if="selectedImage" class="mb-4">
          <img :src="previewUrl" alt="Preview" class="w-full h-48 object-cover rounded-lg" />
          <button
            type="button"
            @click="removeImage"
            class="mt-2 text-red-500 hover:text-red-700 text-sm"
          >
            Remove Image
          </button>
        </div>
        
        <div class="flex justify-end space-x-3">
          <button
            type="button"
            @click="close"
            class="px-4 py-2 text-gray-600 hover:text-gray-800"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="!canSubmit || isLoading"
            class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ isLoading ? 'Posting...' : 'Post' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { usePostsStore } from '@/stores/posts';

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['close', 'posted']);

const postsStore = usePostsStore();

const caption = ref('');
const selectedImage = ref(null);
const previewUrl = ref('');
const isLoading = ref(false);

const canSubmit = computed(() => {
  return caption.value.trim() || selectedImage.value;
});

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedImage.value = file;
    previewUrl.value = URL.createObjectURL(file);
    
    console.log('Selected image:', {
      name: file.name,
      size: file.size,
      type: file.type
    });
  }
};

const removeImage = () => {
  selectedImage.value = null;
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value);
    previewUrl.value = '';
  }
};

const close = () => {
  emit('close');
};

const handleSubmit = async () => {
  if (!canSubmit.value) return;
  
  isLoading.value = true;
  
  try {
    const formData = new FormData();
    
    // Add caption if provided
    if (caption.value.trim()) {
      formData.append('caption', caption.value.trim());
    }
    
    // FIXED: Use 'image' instead of 'img' to match Django model
    if (selectedImage.value) {
      formData.append('image', selectedImage.value);
    }
    
    // Debug: Log FormData contents
    console.log('FormData being sent:');
    for (let [key, value] of formData.entries()) {
      console.log(`${key}:`, value);
    }
    
    const result = await postsStore.createPost(formData);
    
    if (result.success) {
      console.log('Post created successfully!', result.data);
      emit('posted');
      close();
    } else {
      console.error('Failed to create post:', result.error);
      alert('Failed to create post: ' + result.error);
    }
  } catch (error) {
    console.error('Error creating post:', error);
    alert('Error creating post: ' + error.message);
  } finally {
    isLoading.value = false;
  }
};

// Reset form when modal closes
watch(() => props.show, (newVal) => {
  if (!newVal) {
    caption.value = '';
    selectedImage.value = null;
    if (previewUrl.value) {
      URL.revokeObjectURL(previewUrl.value);
      previewUrl.value = '';
    }
  }
});
</script>

<style scoped>
/* Add any additional styles here */
</style>