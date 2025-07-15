import { defineStore } from 'pinia';
import api from '@/services/api';

export const usePostsStore = defineStore('posts', {
  state: () => ({
    feedPosts: [], // Posts from people you follow + your own posts
    myPosts: [], // Only your posts
    currentPost: null,
    isLoading: false,
    isMyPostsLoading: false,
    error: null,
    hasMore: true,
    myPostsHasMore: true,
    feedPage: 1,
    myPostsPage: 1,
  }),
  
  getters: {
    // Get current user ID from localStorage or auth store
    currentUserId: () => parseInt(localStorage.getItem('user_id')),
    currentUsername: () => localStorage.getItem('username'),
  },
  
  actions: {
    async fetchFeed(page = 1) {
      this.isLoading = true;
      this.error = null;
      
      try {
        const response = await api.getPosts(page);
        
        console.log('Feed API response:', response.data);
        
        // Handle DRF pagination format: { count, next, previous, results: [...] }
        const newPosts = Array.isArray(response.data.results) ? response.data.results : [];

        if (page === 1) {
          this.feedPosts = newPosts;
        } else {
          // Append for pagination
          this.feedPosts = [...this.feedPosts, ...newPosts];
        }
        
        this.feedPage = page;
        // Check if there's a 'next' URL to determine if more pages exist
        this.hasMore = response.data.next !== null; 
        
        return { success: true };
      } catch (error) {
        this.error = error.response?.data?.error || error.message;
        console.error('Failed to fetch feed:', error);
        return { success: false, error: error.message };
      } finally {
        this.isLoading = false;
      }
    },
    
    async fetchMyPosts(page = 1) {
      this.isMyPostsLoading = true;
      this.error = null;
      
      try {
        const response = await api.getMyPosts(page);
        
        console.log('My posts API response:', response.data);
        
        // Handle DRF pagination format: { count, next, previous, results: [...] }
        const newPosts = Array.isArray(response.data.results) ? response.data.results : [];

        if (page === 1) {
          this.myPosts = newPosts;
        } else {
          // Append for pagination
          this.myPosts = [...this.myPosts, ...newPosts];
        }
        
        this.myPostsPage = page;
        // Check if there's a 'next' URL to determine if more pages exist
        this.myPostsHasMore = response.data.next !== null; 
        
        return { success: true, data: this.myPosts };
      } catch (error) {
        this.error = error.response?.data?.error || error.message;
        console.error('Failed to fetch my posts:', error);
        return { success: false, error: error.message };
      } finally {
        this.isMyPostsLoading = false;
      }
    },
    
    async loadMoreFeedPosts() {
      if (!this.hasMore || this.isLoading) return;
      return await this.fetchFeed(this.feedPage + 1);
    },
    
    async loadMoreMyPosts() {
      if (!this.myPostsHasMore || this.isMyPostsLoading) return;
      return await this.fetchMyPosts(this.myPostsPage + 1);
    },
    
    async fetchUserPosts(username) {
      try {
        const response = await api.getUserPosts(username);
        
        console.log('User posts API response:', response.data);
        
        // Handle both paginated and direct array responses
        const userPostsData = Array.isArray(response.data.results) ? response.data.results : response.data;
        return { 
          success: true, 
          data: Array.isArray(userPostsData) ? userPostsData : [] 
        };
      } catch (error) {
        console.error('Failed to fetch user posts:', error);
        return { success: false, error: error.response?.data?.error || error.message };
      }
    },
    
    async createPost(formData) {
      try {
        console.log('Creating post with FormData...');
        
        // Log FormData contents for debugging
        for (let [key, value] of formData.entries()) {
          console.log(`FormData ${key}:`, value);
        }
        
        const response = await api.createPost(formData);
        
        console.log('Post created successfully:', response.data);
        
        // Add the new post to the beginning of both arrays if it's your post
        if (response.data) {
          // Add to feed posts
          this.feedPosts.unshift(response.data);
          // Add to my posts
          this.myPosts.unshift(response.data);
        }
        
        return { success: true, data: response.data };
      } catch (error) {
        console.error('Failed to create post:', error);
        console.error('Create post error details:', error.response?.data);
        return { 
          success: false, 
          error: error.response?.data?.error || error.message 
        };
      }
    },
    
    async deletePost(postId) {
      try {
        await api.deletePost(postId);
        
        // Remove from both arrays
        this.feedPosts = this.feedPosts.filter(post => post.pk !== postId);
        this.myPosts = this.myPosts.filter(post => post.pk !== postId);
        
        console.log('Post deleted successfully');
        return { success: true };
      } catch (error) {
        console.error('Failed to delete post:', error);
        return { success: false, error: error.response?.data?.error || error.message };
      }
    },
    
    async toggleLike(postId) {
      try {
        const response = await api.likePost(postId);
        const currentUserId = this.currentUserId;
        
        console.log('Like toggle response:', response.data);
        
        // Update in feedPosts
        const feedPostIndex = this.feedPosts.findIndex(p => p.pk === postId);
        if (feedPostIndex !== -1) {
          const post = this.feedPosts[feedPostIndex];
          
          if (response.data.liked) {
            // Add user to likes array if not already present
            if (!post.likes.includes(currentUserId)) {
              post.likes.push(currentUserId);
            }
          } else {
            // Remove user from likes array
            post.likes = post.likes.filter(id => id !== currentUserId);
          }
          
          // Update likes count
          post.likes_count = response.data.likes_count;
        }
        
        // Update in myPosts if it exists there
        const myPostIndex = this.myPosts.findIndex(p => p.pk === postId);
        if (myPostIndex !== -1) {
          const post = this.myPosts[myPostIndex];
          
          if (response.data.liked) {
            // Add user to likes array if not already present
            if (!post.likes.includes(currentUserId)) {
              post.likes.push(currentUserId);
            }
          } else {
            // Remove user from likes array
            post.likes = post.likes.filter(id => id !== currentUserId);
          }
          
          // Update likes count
          post.likes_count = response.data.likes_count;
        }
        
        return { success: true, data: response.data };
      } catch (error) {
        console.error('Failed to toggle like:', error);
        return { success: false, error: error.response?.data?.error || error.message };
      }
    },
    
    async addComment(postId, text) {
      try {
        const response = await api.commentOnPost(postId, text);
        const currentUsername = this.currentUsername;
        
        console.log('Comment added response:', response.data);
        
        // Create comment object based on response or construct optimistically
        const newComment = {
          pk: response.data.pk || Date.now(), // Use response pk or fallback
          user: currentUsername || 'You',
          text: text,
          created_at: response.data.created_at || new Date().toISOString()
        };
        
        // Add comment to feedPosts
        const feedPost = this.feedPosts.find(p => p.pk === postId);
        if (feedPost && response.data) {
          feedPost.comments.push(newComment);
          feedPost.comments_count = (feedPost.comments_count || 0) + 1;
        }
        
        // Add comment to myPosts if it exists there
        const myPost = this.myPosts.find(p => p.pk === postId);
        if (myPost && response.data) {
          myPost.comments.push(newComment);
          myPost.comments_count = (myPost.comments_count || 0) + 1;
        }
        
        return { success: true, data: response.data };
      } catch (error) {
        console.error('Failed to add comment:', error);
        return { success: false, error: error.response?.data?.error || error.message };
      }
    },
    
    // Helper method to refresh data
    async refreshFeed() {
      this.feedPage = 1;
      this.hasMore = true;
      this.feedPosts = []; // Clear current posts before refreshing
      return await this.fetchFeed(1);
    },
    
    async refreshMyPosts() {
      this.myPostsPage = 1;
      this.myPostsHasMore = true;
      this.myPosts = []; // Clear current posts before refreshing
      return await this.fetchMyPosts(1);
    },
    
    // Helper method to find a post by ID across all arrays
    findPostById(postId) {
      return this.feedPosts.find(p => p.pk === postId) || 
             this.myPosts.find(p => p.pk === postId) || 
             null;
    },
    
    // Helper method to update a post across all arrays
    updatePostInAllArrays(postId, updateFn) {
      // Update in feedPosts
      const feedPostIndex = this.feedPosts.findIndex(p => p.pk === postId);
      if (feedPostIndex !== -1) {
        updateFn(this.feedPosts[feedPostIndex]);
      }
      
      // Update in myPosts
      const myPostIndex = this.myPosts.findIndex(p => p.pk === postId);
      if (myPostIndex !== -1) {
        updateFn(this.myPosts[myPostIndex]);
      }
    },
    
    // Clear all data (useful for logout)
    clearAllData() {
      this.feedPosts = [];
      this.myPosts = [];
      this.currentPost = null;
      this.error = null;
      this.hasMore = true;
      this.myPostsHasMore = true;
      this.feedPage = 1;
      this.myPostsPage = 1;
    },
  },
});