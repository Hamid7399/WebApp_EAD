import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { initClickstreamTracker } from './utils/clickstreamtracker';

// Start tracking before app mount so login/signup are also tracked
initClickstreamTracker();

createApp(App)
  .use(router)
  .mount('#app');
