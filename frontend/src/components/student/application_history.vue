<script setup>
import { ref, onMounted, computed } from 'vue';
import { useStore } from 'vuex';
import api from '@/services/api';

const store = useStore();
const applications = ref([]);
const loading = ref(true);
const error = ref('');
const isDownloading = ref(false);
const downloadMessage = ref('');

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

const downloadHistory = async () => {
    if (isDownloading.value) return;
    
    try {
        isDownloading.value = true;
        downloadMessage.value = 'Initiating download...';
        
        const studentId = store.getters['user/getStudentId'];
        
        const res = await api.post(`/api/student/${studentId}/export_applications`);
        const taskId = res.data.task_id;
        
        const checkStatus = async () => {
            try {
                const statusRes = await api.get(`/api/task_status/${taskId}`);
                if (statusRes.data.state === 'SUCCESS') {
                    downloadMessage.value = 'Downloading file...';
                    
                    const fileRes = await api.get(`/api/download/${taskId}`, { responseType: 'blob' });
                    const url = window.URL.createObjectURL(new Blob([fileRes.data]));
                    const link = document.createElement('a');
                    link.href = url;
                    link.setAttribute('download', 'application_history.csv');
                    document.body.appendChild(link);
                    link.click();
                    link.remove();
                    
                    isDownloading.value = false;
                    downloadMessage.value = '';
                } else if (statusRes.data.state === 'FAILURE') {
                    error.value = 'Failed to generate download. Please try again later.';
                    isDownloading.value = false;
                    downloadMessage.value = '';
                } else {
                    downloadMessage.value = 'Generating CSV...';
                    setTimeout(checkStatus, 2000);
                }
            } catch (err) {
                console.error('Error checking task status:', err);
                error.value = 'Error generating download. Please try again.';
                isDownloading.value = false;
                downloadMessage.value = '';
            }
        };
        
        setTimeout(checkStatus, 1500);
        
    } catch (err) {
        console.error('Error starting export task:', err);
        error.value = 'Failed to start download. Please try again later.';
        isDownloading.value = false;
        downloadMessage.value = '';
    }
};
</script>

<template>
    <div class="container mt-4 mb-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fw-bold text-dark m-0">Application History</h2>
            <button @click="downloadHistory" :disabled="isDownloading" class="btn btn-outline-primary d-flex align-items-center gap-2 shadow-sm">
                <span v-if="isDownloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                <i v-else class="bi bi-download"></i>
                {{ isDownloading ? downloadMessage : 'Download History (CSV)' }}
            </button>
        </div>
        
        <div v-if="loading" class="text-center my-5 py-5">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h5 class="mt-3 text-muted">Retrieving history...</h5>
        </div>

        <div v-else-if="error" class="alert alert-danger shadow-sm border-0 rounded-3">
            <i class="bi bi-exclamation-triangle-fill me-2"></i> {{ error }}
        </div>

        <div v-else-if="pastApplications.length === 0" class="alert alert-info shadow-sm border-0 rounded-3">
            <i class="bi bi-info-circle-fill me-2"></i> You have no past applications at this time.
        </div>

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
