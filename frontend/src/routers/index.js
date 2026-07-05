import Register from '@/components/Register.vue'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import navbar from '@/components/navbar.vue'
import Admin from '@/components/admin_dashboard.vue'
import AdminHome from '@/components/admin/admin_home.vue'
import RegistrationRequests from '@/components/admin/registration_requests.vue'
import DriveRequests from '@/components/admin/drive_request.vue'
import CompanyDetails from '@/components/company_details.vue'
import DriveDetails from '@/components/drive_details.vue'
import StudentProfile from '@/components/student_details.vue'
import EditStudent from '@/components/admin/edit_student.vue'
import StudentList from '@/components/admin/students_list.vue'
import CompanyList from '@/components/admin/company_list.vue'
import DriveList from '@/components/admin/drive_list.vue'
import EditCompany from '@/components/admin/edit_company.vue'
import {createRouter, createWebHistory} from 'vue-router'
import store from '@/store/index'

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
        component: navbar,
        meta: { requiresAuth: true }
    },
    {
        path: '/admin',
        name: 'Admin',
        component: Admin,
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
            {
                path: '',
                name: 'AdminHome',
                component: AdminHome,
            },
            {
                path: 'registration-requests',
                name: 'RegistrationRequests',
                component: RegistrationRequests,
            },
            {
                path: 'drive-requests',
                name: 'DriveRequests',
                component: DriveRequests,
            },
            {
                path: 'students',
                name: 'StudentList',
                component: StudentList,
            },
            {
                path: 'companies',
                name: 'CompanyList',
                component: CompanyList,
            },
            {
                path: 'placement-drives',
                name: 'DriveList',
                component: DriveList   
            },
            {
                path: 'search',
                name: 'AdminSearch',
                component: () => import('@/components/admin/admin_search.vue')
            }
        ]
    },
    {
        path: '/company',
        name: 'CompanyDashboard',
        component: navbar,
        children: [
            {
                path: ':id',
                name: 'CompanyDetails',
                component: CompanyDetails,
                children: [
                    {
                        path: 'edit',
                        name: 'EditCompany',
                        component: EditCompany
                    }
                ]
            },
            {
                path: 'placement-drives',
                name: 'CompanyDriveList',
                component: DriveList
            }
        ]
    },
    {
        path: '/placement-drive/:id',
        name: 'DriveDetails',
        component: DriveDetails
    },
    {
        path: '/placement-drive/:id/edit',
        name: 'EditDrive',
        component: () => import('@/components/admin/edit_drive.vue')
    },
    {
        path: '/student/:id',
        name: 'StudentProfile',
        component: StudentProfile
    },
    {
        path: '/student/:id/edit',
        name: 'EditStudent',
        component: EditStudent
    }
]



const router = createRouter({routes, history: createWebHistory()})

// Route guards
router.beforeEach((to, from) => {
    const isAuthenticated = store.getters['user/isAuthenticated'];
    const isAdmin = store.getters['user/isAdmin'];
    const user = store.getters['user/getUser'];

    console.log(`[Router Guard] Navigating to: ${to.name}, isAuth: ${isAuthenticated}, isAdmin: ${isAdmin}, user: ${user?.email}`);

    // Check if route requires authentication
    if (to.meta.requiresAuth && !isAuthenticated) {
        console.log(`[Router Guard] Route requires auth but user not authenticated, redirecting to Login`);
        return { name: 'Login', query: { redirect: to.fullPath } };
    }

    // Check if route requires admin role
    if (to.meta.requiresAdmin && !isAdmin) {
        console.log(`[Router Guard] Route requires admin but user is not admin, redirecting to Home`);
        return { name: 'Home' };
    }

    // Redirect authenticated users with valid user data away from login/register
    if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated && user) {
        const redirect = isAdmin ? 'AdminHome' : 'Dashboard';
        console.log(`[Router Guard] Authenticated user on ${to.name}, redirecting to ${redirect}`);
        return { name: redirect };
    }
});

export default router