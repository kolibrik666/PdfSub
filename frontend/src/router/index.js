import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import SignUpView from '../views/SignUpView.vue'
import AdminView from '../views/AdminView.vue'
import PublicationDetailView from '../views/PublicationDetailView.vue';
import ManagePublicationsView from '../views/ManagePublicationsView.vue';
import StudentPublicationsView from '../views/StudentPublicationsView.vue';
import LandingPageView from '@/views/LandingPageView.vue'

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
    path: '/sign_up',
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
    path: '/manage-publications',
    name: 'manage-publications',
    component: ManagePublicationsView,
    meta: { requiresAdmin: true }
  },
  {
    path: '/publication/:id',
    name: 'publication-detail',
    component: PublicationDetailView,
  },
  {
    path: '/student-publications',
    name: 'student-publications',
    component: StudentPublicationsView,
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

router.beforeEach((to, from, next) => {
  const isAdmin = localStorage.getItem('isAdmin') === 'true';
  if (to.matched.some(record => record.meta.requiresAdmin)) {
    if (isAdmin) {
      next();
    } else {
      next({ name: 'home' });
    }
  } else {
    next();
  }
});

export default router
