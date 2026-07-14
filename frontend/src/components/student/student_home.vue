<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useStore } from 'vuex';
import api from '@/services/api';

const router = useRouter();
const route = useRoute();
const store = useStore();

let errorMessage = ref('');
let activeApplications = ref([]);

onMounted(() => {
    fetchApplications();
});

async function fetchApplications() {
    try {
        const studentId = store.getters['user/getStudentId'];
        const res = await api.get(`/api/student/${studentId}/applications`);
        activeApplications.value = res.data.applications;
    } catch(err) {
        if (err.response && err.response.data.message) {
            errorMessage.value = err.response.data.message;
        } else {
            errorMessage.value = 'Error fetching applications';
        }
    }
}

const notRejectedApplications = computed(() => {
    return activeApplications.value.filter(app => app.status !== 'rejected' && app.status !== 'Rejected');
});

const upcomingInterviewsThisMonth = computed(() => {
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    return activeApplications.value.filter(app => {
        if (!app.interview_date) return false;
        const interviewDate = new Date(app.interview_date);
        return interviewDate >= startOfToday && 
               interviewDate.getMonth() === currentMonth && 
               interviewDate.getFullYear() === currentYear;
    }).sort((a, b) => new Date(a.interview_date) - new Date(b.interview_date));
});

const getStatusBadgeClass = (status) => {
    const s = status.toLowerCase();
    if (s === 'applied') return 'badge bg-primary';
    if (s === 'shortlisted') return 'badge bg-info text-dark';
    if (s === 'selected (for interview)') return 'badge bg-warning text-dark';
    if (s === 'offered' || s === 'placed') return 'badge bg-success';
    if (s === 'rejected') return 'badge bg-danger';
    return 'badge bg-secondary';
};
</script>

<template>
    <div class="container mt-4">
        
        <div v-if="upcomingInterviewsThisMonth.length > 0" class="mb-5">
            <h3 class="mb-4 fw-bold text-dark">Upcoming Interviews</h3>
            <div class="row">
                <div class="col-md-6 col-lg-4 mb-4" v-for="app in upcomingInterviewsThisMonth" :key="'interview-' + app.id">
                    <div class="card h-100 shadow-sm border-0 border-start border-warning border-4 application-card">
                        <div class="card-body d-flex flex-column">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div>
                                    <h5 class="card-title text-primary mb-1 fw-bold">{{ app.company_name }}</h5>
                                    <h6 class="card-subtitle text-muted">{{ app.job_title }}</h6>
                                </div>
                                <span class="badge bg-warning text-dark rounded-pill px-3 py-2">
                                    <i class="bi bi-calendar-event me-1"></i>
                                    {{ new Date(app.interview_date).toLocaleDateString() }}
                                </span>
                            </div>
                            
                            <div class="mt-auto pt-3 border-top">
                                <router-link :to="`/application/${app.id}`" class="btn btn-outline-warning text-dark btn-sm w-100 fw-semibold">View Details</router-link>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <h2 class="mb-4 fw-bold text-dark">Active Applications</h2>
        
        <div v-if="errorMessage" class="alert alert-danger shadow-sm">
            {{ errorMessage }}
        </div>

        <div v-if="!activeApplications.length" class="alert alert-info shadow-sm">
            You have not applied to any placement drives yet.
        </div>
        <div v-else-if="!notRejectedApplications.length" class="alert alert-info shadow-sm">
            No active applications found.
        </div>
        
        <div class="row" v-else>
            <div class="col-md-6 col-lg-4 mb-4" v-for="app in notRejectedApplications" :key="app.id">
                <div class="card h-100 shadow-sm border-0 application-card">
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-start mb-2">
                            <div>
                                <h5 class="card-title text-primary mb-1 fw-bold">{{ app.company_name }}</h5>
                                <h6 class="card-subtitle text-muted">{{ app.job_title }}</h6>
                            </div>
                            <span :class="getStatusBadgeClass(app.status) + ' rounded-pill px-3 py-2'">
                                {{ app.status }}
                            </span>
                        </div>
                        
                        <div class="mt-auto pt-3 border-top d-flex flex-column">
                            <div class="d-flex justify-content-between text-muted small align-items-center mb-2">
                                <span><i class="bi bi-calendar3"></i> Applied: {{ new Date(app.date).toLocaleDateString() }}</span>
                                <span class="text-secondary fw-semibold">App ID: #{{ app.id }}</span>
                            </div>
                            <div v-if="app.interview_date" class="text-muted small mb-3">
                                <strong>Interview:</strong> {{ new Date(app.interview_date).toLocaleDateString() }}
                            </div>
                            <router-link :to="`/application/${app.id}`" class="btn btn-outline-primary btn-sm w-100 fw-semibold">View Details</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.application-card {
    transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
    border-radius: 12px;
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
}
.application-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.08) !important;
}
.badge {
    font-size: 0.85em;
    text-transform: capitalize;
}
</style>