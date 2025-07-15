// stores/profile.js
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useProfileStore = defineStore('profile', {
  state: () => ({
    currentProfile: null,
    isLoading: false,
    error: null,
  }),
  
  actions: {
    async fetchProfile(username) {
      this.isLoading = true;
      this.error = null;
      
      try {
        console.log('Fetching profile for:', username);
        
        const response = username 
          ? await api.getUserProfile(username)
          : await api.getMyProfile();
          
        this.currentProfile = response.data;
        console.log('Profile fetched successfully:', response.data);
        
        return { success: true, data: response.data };
      } catch (error) {
        this.error = error.response?.data?.error || error.message;
        console.error('Failed to fetch profile:', error);
        return { success: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },
    
    async updateProfile(profileData) {
      this.isLoading = true;
      this.error = null;
      
      try {
        console.log('Updating profile with:', profileData);
        
        // Log FormData contents if it's FormData
        if (profileData instanceof FormData) {
          console.log('FormData contents:');
          for (let [key, value] of profileData.entries()) {
            console.log(`${key}:`, value);
          }
        }
        
        const response = await api.updateProfile(profileData);
        this.currentProfile = response.data;
        
        console.log('Profile updated successfully:', response.data);
        
        return { success: true, data: response.data };
      } catch (error) {
        this.error = error.response?.data?.error || error.message;
        console.error('Failed to update profile:', error);
        console.error('Error details:', error.response?.data);
        return { success: false, error: this.error };
      } finally {
        this.isLoading = false;
      }
    },
    
    async toggleFollow(username) {
      try {
        console.log('Toggling follow for:', username);
        
        const response = await api.followUser(username);
        
        console.log('Follow toggle response:', response.data);
        
        return { 
          success: true, 
          following: response.data.following,
          followers_count: response.data.followers_count
        };
      } catch (error) {
        console.error('Failed to toggle follow:', error);
        return { success: false, error: error.response?.data?.error || error.message };
      }
    },

    clearProfile() {
      this.currentProfile = null;
      this.error = null;
    }
  },
});