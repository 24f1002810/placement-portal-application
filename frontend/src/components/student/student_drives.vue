<script setup>
import { ref, computed, onMounted } from 'vue';
import api from '@/services/api';

const drives = ref([]);
const searchQuery = ref('');
const loading = ref(true);
const error = ref('');

onMounted(async () => {
    try {
        const response = await api.get('/api/student/placement-drives');
        drives.value = response.data.drives;
    } catch (err) {
        console.error('Error fetching drives:', err);
        error.value = 'Failed to load placement drives. Please try again later.';
    } finally {
        loading.value = false;
    }
});

const filteredDrives = computed(() => {
    if (!searchQuery.value) return drives.value;
    const query = searchQuery.value.toLowerCase();
    return drives.value.filter(drive => 
        (drive.job_title && drive.job_title.toLowerCase().includes(query)) ||
        (drive.company_name && drive.company_name.toLowerCase().includes(query))
    );
});

const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    return new Date(dateString).toLocaleDateString();
};
</script>

<template>
    <div class="container mt-4 mb-5">
        <h2 class="mb-4 fw-bold text-dark">Active Placement Drives</h2>
        
        <!-- Search Bar -->
        <div class="row mb-4">
            <div class="col-md-8 col-lg-6">
                <div class="input-group shadow-sm search-group">
                    <span class="input-group-text bg-white border-end-0 text-primary">
                        <i class="bi bi-search"></i>
                    </span>
                    <input 
                        type="text" 
                        class="form-control border-start-0 ps-0 fw-medium" 
                        placeholder="Search by Job Title or Company Name..." 
                        v-model="searchQuery"
                    >
                </div>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center my-5 py-5">
            <div class="spinner-border text-primary" role="status" style="width: 3rem; height: 3rem;">
                <span class="visually-hidden">Loading...</span>
            </div>
            <h5 class="mt-3 text-muted">Discovering Opportunities...</h5>
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="alert alert-danger shadow-sm border-0 rounded-3">
            <i class="bi bi-exclamation-triangle-fill me-2"></i> {{ error }}
        </div>

        <!-- Empty State -->
        <div v-else-if="filteredDrives.length === 0" class="alert alert-info shadow-sm border-0 rounded-3">
            <i class="bi bi-info-circle-fill me-2"></i> No active drives found matching your search.
        </div>

        <!-- Drive Cards -->
        <div class="row" v-else>
            <div class="col-md-6 col-xl-4 mb-4" v-for="drive in filteredDrives" :key="drive.id">
                <div class="card h-100 shadow-sm border-0 drive-card hover-elevate">
                    <div class="card-body d-flex flex-column p-4">
                        <div class="mb-3">
                            <h4 class="card-title text-primary fw-bold mb-1 text-truncate" :title="drive.job_title">
                                {{ drive.job_title }}
                            </h4>
                            <h6 class="card-subtitle text-secondary fw-semibold mb-3">
                                <i class="bi bi-building me-1"></i> {{ drive.company_name }}
                            </h6>
                        </div>
                        
                        <p class="card-text text-muted small mb-4 flex-grow-1" style="display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">
                            {{ drive.job_description }}
                        </p>

                        <div class="mt-auto pt-3 border-top">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <div class="text-muted small">
                                    <i class="bi bi-calendar-x text-danger"></i> Deadline<br>
                                    <span class="fw-bold text-dark">{{ formatDate(drive.deadline) }}</span>
                                </div>
                                <div class="text-muted small text-end">
                                    <i class="bi bi-cash-stack text-success"></i> Salary<br>
                                    <span class="fw-bold text-dark">₹{{ drive.salary }}</span>
                                </div>
                            </div>
                            <router-link :to="`/placement-drive/${drive.id}`" class="btn btn-primary w-100 fw-bold rounded-pill shadow-sm">
                                View Details & Apply <i class="bi bi-arrow-right ms-1"></i>
                            </router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.drive-card {
    transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    border-radius: 16px;
    background: linear-gradient(145deg, #ffffff, #f8f9fa);
}
.hover-elevate:hover {
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.12) !important;
}
.search-group {
    border-radius: 50rem;
    overflow: hidden;
}
.search-group .input-group-text, 
.search-group .form-control {
    border-color: #e9ecef;
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
}
.search-group .form-control:focus {
    border-color: #e9ecef;
    box-shadow: none;
}
.search-group:focus-within {
    box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15) !important;
}
</style>
