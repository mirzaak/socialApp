import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'
// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyD-CwW2eYDoyN3FIchrsl_mcWaatU0ZpVo",
  authDomain: "socialapp-c4c99.firebaseapp.com",
  projectId: "socialapp-c4c99",
  storageBucket: "socialapp-c4c99.appspot.com",
  messagingSenderId: "447953496949",
  appId: "1:447953496949:web:9a27b85dde38021b3a813c",
  measurementId: "G-Q9EE731Q7V"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const pinia = createPinia()

createApp(App).use(router).use(bootstrap).use(pinia).mount('#app')

