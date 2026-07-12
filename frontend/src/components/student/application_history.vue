<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import api from '@/services/api';

const store = useStore();
const applications = ref([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
    try {
        const studentId = store.getters['user/getStudentId'];
        const res = await api.get(`/api/student/${studentId}/applications`);
        applications.value = res.data.applications;
    } catch (err) {
        console.error('Error fetching application history:', err);
        error.value = 'Failed to load application history. Please try again later.';
    } finally {
        loading.value = false;
    }
});

const pastApplications = computed(() => {
    const pastStatuses = ['rejected', 'placed'];
    return applications.value.filter(app => 
        pastStatuses.includes(app.status?.toLowerCase())
    );
});

const getStatusBadgeClass = (status) => {
    const s = (status || '').toLowerCase();
    if (s === 'placed') return 'badge bg-success';
    if (s === 'rejected') return 'badge bg-danger';
    return 'badge bg-secondary';
};

const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
};
</script>

<template>
    <div class="container mt-4 mb-5">
        <h2 class="mb-4 fw-bold text-dark">Application History</h2>
        
        <!-- Loading State -->
        <div v-if="loading" class="text-center my-5 py-5">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h5 class="mt-3 text-muted">Retrieving history...</h5>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="alert alert-danger shadow-sm border-0 rounded-3">
            <i class="bi bi-exclamation-triangle-fill me-2"></i> {{ error }}
        </div>

        <!-- Empty State -->
        <div v-else-if="pastApplications.length === 0" class="alert alert-info shadow-sm border-0 rounded-3">
            <i class="bi bi-info-circle-fill me-2"></i> You have no past applications at this time.
        </div>

        <!-- Table View -->
        <div v-else class="card shadow-sm border-0 rounded-4 overflow-hidden">
            <div class="card-body p-0">
                <div class="table-responsive">
                    <table class="table table-hover table-striped align-middle mb-0">
                        <thead class="table-dark">
                            <tr>
                                <th class="ps-4">Company</th>
                                <th>Job Title</th>
                                <th>Applied On</th>
                                <th>Interview Date</th>
                                <th>Status</th>
                                <th class="text-end pe-4">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="app in pastApplications" :key="app.id">
                                <td class="ps-4 fw-semibold">{{ app.company_name }}</td>
                                <td>{{ app.job_title }}</td>
                                <td>{{ formatDate(app.date) }}</td>
                                <td>{{ formatDate(app.interview_date) }}</td>
                                <td>
                                    <span :class="getStatusBadgeClass(app.status) + ' px-3 py-2 rounded-pill text-capitalize shadow-sm'">
                                        {{ app.status }}
                                    </span>
                                </td>
                                <td class="text-end pe-4">
                                    <router-link :to="`/application/${app.id}`" class="btn btn-sm btn-outline-primary fw-semibold rounded-pill px-3">
                                        View Details
                                    </router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.table th {
    font-weight: 600;
    letter-spacing: 0.5px;
    padding-top: 1rem;
    padding-bottom: 1rem;
}
.table td {
    padding-top: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #f1f1f1;
}
</style>
