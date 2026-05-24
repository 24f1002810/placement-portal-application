import Register from '@/components/Register.vue'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Dashboard from '@/components/Dashboard.vue'
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {path: '/',
        name: 'Home',
        component: Home
    },
    {path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
    },
    {
        path: '/dashboard',
        name: 'Dashboard',
        component: Dashboard
    }
]

const router = createRouter({routes, history: createWebHistory()})
export default router
