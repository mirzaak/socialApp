import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

import 'bootstrap-icons/font/bootstrap-icons';
import 'bootstrap/dist/css/bootstrap.css'
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js'
const pinia = createPinia()
createApp(App).use(router).use(bootstrap).use(pinia).mount('#app')

