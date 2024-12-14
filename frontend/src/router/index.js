import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import AdminView from '../views/AdminView.vue'
import PublicationDetailView from '../views/PublicationDetailView.vue';
import LandingPageView from '@/views/LandingPageView.vue'
import ReviewerView from '@/views/ReviewerView.vue';
import ReviewView from '@/views/ReviewView.vue';
import PublicationsView from "@/views/PublicationsView.vue";

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
    meta: { requiresAdmin: true }
  },
  {
    path: '/publication/:id',
    name: 'publication-detail',
    component: PublicationDetailView,
  },
  {
    path: '/publications',
    name: 'publications',
    component: PublicationsView,
  },
  {
    path: '/reviewer',
    name: 'reviewer',
    component: ReviewerView,
  },
  {
    path: '/review/:paper_id',
    name: 'review',
    component: ReviewView,
  },
  {
    path: '/landing-page',
    name: 'landing-page',
    component: LandingPageView,
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
  }
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
  } else {
    next();
  }
});

export default router
