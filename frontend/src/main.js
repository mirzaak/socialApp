import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';
import router from './router';
import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';
import './assets/styles/main.css';

const app = createApp(App);
const pinia = createPinia();

// Toast options
const toastOptions = {
  position: 'top-right',
  timeout: 3000,
  closeOnClick: true,
  pauseOnFocusLoss: true,
  pauseOnHover: true,
  draggable: true,
  draggablePercent: 0.6,
  showCloseButtonOnHover: false,
  hideProgressBar: false,
  closeButton: 'button',
  icon: true,
  rtl: false,
  transition: 'Vue-Toastification__bounce',
  maxToasts: 5,
  newestOnTop: true
};
// In main.js
import CreatePostModal from './components/posts/CreatePostModal.vue';

app.component('CreatePostModal', CreatePostModal);
app.use(pinia);
app.use(router);
app.use(Toast, toastOptions);

app.mount('#app');

