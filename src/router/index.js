import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    redirect:'/Home'
  },
  {
    path: '/Home',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/user/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/user/Register.vue')
  },
  {
    path: '/findpassword',
    name: 'Findpassword',
    component: () => import('../views/user/Findpassword.vue')
  },
  {
    path:'/about',
    name:"About",
    component:()=>import("../views/About.vue")
  },
  {
    path:'/test3d',
    name:"test3d",
    component:()=>import("../views/test3d.vue")
  },
  {
    path:'/test2d',
    name:"test2d",
    component:()=>import("../views/test2d.vue")
  },
  {
    path: '/func',
    name: 'Func',
    component: () => import('../views/Func.vue')
  },
  {
    path: '/projSel',
    name: 'ProjSel',
    component: () => import('../views/ProjSel.vue')
  },
  {
    path: '/charts',
    name: 'charts',
    component: () => import('../views/Charts.vue')
  },
]

const router = new VueRouter({
  routes
})

export default router
