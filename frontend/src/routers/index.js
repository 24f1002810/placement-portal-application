import Register from '@/components/Register.vue'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Dashboard from '@/components/Dashboard.vue'
import Admin from '@/components/admin.vue'
import AdminHome from '@/components/admin_home.vue'
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
    },
    {
        path: '/admin',
        name: 'Admin',
        component: Admin,
        children: [
            {
                path: '',
                name: 'AdminHome',
                component: AdminHome
            }
        ]
    }
]

const router = createRouter({routes, history: createWebHistory()})
export default router
