import Vue from 'vue';
import VueRouter from 'vue-router';
import { getUserRole } from '@/utils/tokenManager';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/components/Login.vue'),
    meta: {
      title: 'Hospital Management - Login',
      requiresAuth: false
    }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: () => import('@/components/AdminDashboard.vue'),
    meta: {
      title: 'Hospital Management - Admin Dashboard',
      requiresAuth: true,
      requiredRole: 'Admin'
    }
  },
  {
    path: '*',
    redirect: '/login'
  }
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
});

// Navigation guard to check authentication and authorization
router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiredRole = to.matched[0]?.meta?.requiredRole;
  const token = localStorage.getItem('token');
  const userRole = getUserRole();

  // Update page title
  if (to.meta.title) {
    document.title = to.meta.title;
  }

  if (requiresAuth) {
    if (!token) {
      // No token, redirect to login
      console.warn('Access denied: No authentication token');
      next('/login');
    } else if (requiredRole && userRole !== requiredRole) {
      // Token exists but user doesn't have required role
      console.warn(`Access denied: Required role ${requiredRole}, but user is ${userRole}`);
      next('/login');
    } else {
      // Token exists and user has required role
      next();
    }
  } else {
    // Route doesn't require auth
    if (token && to.path === '/login') {
      // User is already logged in but trying to access login page
      // Redirect to dashboard
      const role = getUserRole();
      if (role === 'Admin') {
        next('/admin');
      } else {
        next('/login');
      }
    } else {
      next();
    }
  }
});

// Handle after navigation
router.afterEach((to, from) => {
  // You can add analytics, logging, etc. here
  console.log(`Navigated from ${from.path} to ${to.path}`);
});

export default router;
