import { createRouter, createWebHistory } from 'vue-router';
import Login from '../views/LoginPage.vue';
import Signup from '../views/SignUp.vue';
import Dashboard from '../views/UserDashboard.vue';
import PdfView from '../views/PDFview.vue';
import QuizPage from '../views/QuizPage.vue';

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', name: 'Login', component: Login },
  { path: '/signup', name: 'Signup', component: Signup },
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },
  { path: '/pdf', name: 'PdfView', component: PdfView },
  { path: '/quiz', name: 'QuizPage', component: QuizPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
