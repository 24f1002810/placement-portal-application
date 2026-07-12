import Register from '@/components/Register.vue'
import Home from '../components/Home.vue'
import Login from '../components/Login.vue'
import Admin from '@/components/admin_dashboard.vue'
import AdminHome from '@/components/admin/admin_home.vue'
import RegistrationRequests from '@/components/admin/registration_requests.vue'
import DriveRequests from '@/components/admin/drive_request.vue'
import CompanyDetails from '@/components/company/company_details.vue'
import DriveDetails from '@/components/drive_details.vue'
import StudentProfile from '@/components/student/student_details.vue'
import EditStudent from '@/components/admin/edit_student.vue'
import StudentList from '@/components/admin/students_list.vue'
import CompanyList from '@/components/admin/company_list.vue'
import DriveList from '@/components/admin/drive_list.vue'
import EditCompany from '@/components/admin/edit_company.vue'
import ApplicationsList from '@/components/applications.vue'
import ApplicationDetail from '@/components/application_detail.vue'
import { createRouter, createWebHistory } from 'vue-router'
import store from '@/store/index'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/login',
        name: 'Login',
        component: Login
    },
    {
        path: '/register',
        name: 'Register',
        component: Register
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
                path: 'students/:id',
                name: 'ApplicantProfile',
                component: StudentProfile,
                children: [
                    {
                        path: 'edit',
                        name: 'AdminEditStudent',
                        component: EditStudent
                    }
                ]
            },
            {
                path: 'companies',
                name: 'CompanyList',
                component: CompanyList,
            },
            {
                path: 'companies/:id',
                name: 'CompanyProfile',
                component: CompanyDetails,
                children: [
                    {
                        path: 'edit',
                        name: 'AdminEditCompany',
                        component: EditCompany
                    }
                ]
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
            },
            {
                path: 'applications',
                name: 'AdminApplications',
                component: ApplicationsList
            }
        ]
    },
    {
        path: '/company/:id',
        name: 'CompanyDashboard',
        component: () => import('@/components/company_dashboard.vue'),
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                name: 'CompanyHome',
                component: () => import('@/components/company/company_home.vue')
            },
            {
                path: 'create-drive',
                name: 'CreateDrive',
                component: () => import('@/components/company/create_drive.vue')
            },
            {
                path: 'applications',
                name: 'CompanyApplications',
                component: () => import('@/components/applications.vue')
            },
            {
                path: 'profile',
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
            },
            {
                path: 'search',
                name: 'CompanySearch',
                component: () => import('@/components/company/company_search.vue')
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
        name: 'StudentDashboard',
        component: () => import('@/components/student_dashboard.vue'),
        children: [
            {
                path: '',
                name: 'StudentHome',
                component: () => import('@/components/student/student_home.vue')
            },
            {
                path: 'profile',
                name: 'StudentDetails',
                component: StudentProfile,
                children: [
                    {
                        path: 'edit',
                        name: 'EditStudent',
                        component: EditStudent
                    }
                ]
            },
            {
                path: 'applications',
                name: 'StudentApplications',
                component: () => import('@/components/student/application_history.vue')
            },
            {
                path: 'search',
                name: 'StudentSearch',
                component: () => import('@/components/student/student_search.vue')
            },
            {
                path: 'placement-drives',
                name: 'StudentDriveList',
                component: () => import('@/components/student/student_drives.vue')
            },
        ]

    },
    {
        path: '/application/:id',
        name: 'ApplicationDetail',
        component: ApplicationDetail
    }
]



const router = createRouter({ routes, history: createWebHistory() })

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
        let redirectRoute;

        if (user.role === 'admin') {
            redirectRoute = { name: 'AdminHome' };
        } else if (user.role === 'company') {
            redirectRoute = { path: `/company/${user.companyId || user.id}` };
        } else {
            redirectRoute = { name: 'Dashboard' };
        }

        console.log(`[Router Guard] Authenticated user on ${to.name}, redirecting to`, redirectRoute);
        return redirectRoute;
    }
});

export default router