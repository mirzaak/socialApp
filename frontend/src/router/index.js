import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import MyProfile from '../views/MyProfile.vue'
import Profile from '../views/Profile.vue'
import Explore from '../views/Explore.vue'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import Searched from '../views/Searched.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/myprofile',
    name: 'MyProfile',
    component: MyProfile
  },
  {
    path: '/profile/:id',
    name: 'Profile',
    component: Profile
  },
  {
    path: '/explore',
    name: 'Explore',
    component: Explore
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/searched/:search',
    name: 'Searched',
    component: Searched
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
