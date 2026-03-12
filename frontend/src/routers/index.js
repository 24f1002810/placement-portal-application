import Login from '../components/Login.vue'
import {createRouter, createWebHistory} from 'vue-router'

const routes = [
    {router: '/login',
        name: 'Login',
        component: Login
    }
]

const router = createRouter({routes, history: createWebHistory()})
export default router
