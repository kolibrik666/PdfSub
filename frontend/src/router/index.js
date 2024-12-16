import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import AdminView from '../views/AdminView.vue'
import PublicationDetailView from '../views/PublicationDetailView.vue';
import LandingPageView from '@/views/LandingPageView.vue'
import ReviewView from '@/views/ReviewView.vue';
import PublicationsView from "@/views/PublicationsView.vue";
import ConferencesView from "@/views/ConferencesView.vue";
const routes = [
  {
    path: '/',
    name: 'home',
    component: LandingPageView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/sign-up',
    name: 'sign-up',
    component: SignUpView
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminView,
    meta: { requiresAdmin: true , requiresAuth: true }
  },
  {
    path: '/publication/:id',
    name: 'publication-detail',
    component: PublicationDetailView,
    meta: { requiresAuth: true }
  },
  {
    path: '/publications',
    name: 'publications',
    component: PublicationsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/review/:id',
    name: 'review',
    component: ReviewView,
    meta: { requiresAuth: true }
  },
  {
    path: '/landing-page',
    name: 'landing-page',
    component: LandingPageView,
  },
  {
    path: "/conferences",
    name: "Conferences",
    component: ConferencesView,
    meta: { requiresAdmin: true, requiresAuth: true }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

import api from '../services/api';

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('userToken');
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (token) {
      try {
        const response = await api.decode_token({ token });
        const decodedToken = response.data.user;
        const isAdmin = decodedToken.isAdmin;
        if (isAdmin) {
          next();
        } else {
          next({ name: 'home' });
        }
      } catch (error) {
        console.error("Token decoding failed", error.response ? error.response.data : error.message);
        next({ name: 'home' });
      }
    } else {
      next({ name: 'home' });
    }
  } else if (to.matched.some(record => record.meta.requiresAuth)) {
    if (token) {
      try {
        await api.decode_token({ token });
        next();
      } catch (error) {
        console.error("Token decoding failed", error.response ? error.response.data : error.message);
        next({ name: 'login' });
      }
    } else {
      next({ name: 'login' });
    }
  } else {
    next();
  }
});

export default router
