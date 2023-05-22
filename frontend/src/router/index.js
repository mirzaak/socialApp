import { createRouter, createWebHistory } from 'vue-router'
import { useProductStore } from '../stores/user'
import { createPinia } from 'pinia';
import Home from '../views/Home.vue'
import HomeTwo from '../views/HomeTwo.vue'
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
    path: '/',
    name: 'HomeTwo',
    component: HomeTwo
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

router.beforeEach(async (to, from) => {
  const store = useProductStore()
  if (
    // make sure the user is authenticated
    store.isAuthenticated &&
    // ❗️ Avoid an infinite redirect
    to.name == 'Login'
  ) {
    // redirect the user to the login page
    return { name: 'Home' }
  }
})
router.beforeEach(async (to, from) => {
  const store = useProductStore()
  if (
    // make sure the user is authenticated
    store.isAuthenticated &&
    // ❗️ Avoid an infinite redirect
    to.name == 'Home'
  ) {
    // redirect the user to the login page
    return { name: 'HomeTwo' }
  }
})
export default router
