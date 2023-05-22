import { defineStore } from 'pinia'

export const useProductStore = defineStore('user', {
    state: () => ({
        isAuthenticated: false,
        token: '',
        darkMode: false,
    }),
    actions: {
        initializeStore() {
            if (localStorage.getItem('access') && localStorage.getItem('access') != 'undefined') {
                this.token = localStorage.getItem('access')
                this.isAuthenticated = true
            } else {
                this.token = ''
                this.isAuthenticated = false
            }
        }
    }
})