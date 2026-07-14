<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();

const loading = ref(false);
const error = ref('');
const searchResults = ref([]);
const searchQuery = ref('');
const searchType = ref('applications');
const companyId = route.params.id;

const fetchSearchResults = async () => {
    loading.value = true;
    error.value = '';
    searchResults.value = [];
    searchQuery.value = route.query.q || '';
    searchType.value = route.query.type || 'applications';

    try {
        let response;
        let data = [];
        const query = searchQuery.value.toLowerCase();

        if (searchType.value === 'applications') {
            response = await api.get(`api/company/${companyId}/applications`);
            data = response.data.applications;

            searchResults.value = data.filter(app => 
                (app.id && app.id.toString().toLowerCase().includes(query)) ||
                (app.student_name && app.student_name.toLowerCase().includes(query))
            );
        } else if (searchType.value === 'placement-drives') {
            response = await api.get(`api/company/${companyId}/placement-drives`);
            data = response.data.placement_drives;

            searchResults.value = data.filter(drive => 
                (drive.job_title && drive.job_title.toLowerCase().includes(query))
            );
        }
    } catch (err) {
        error.value = err.response?.data?.message || 'Failed to perform search';
        console.error('Search error:', err);
    } finally {
        loading.value = false;
    }
};

onMounted(() => {
    fetchSearchResults();
});

watch(
    () => [route.query.q, route.query.type],
    () => {
        fetchSearchResults();
    }
);
</script>

<template>
    <div class="container mt-5 mb-5">
        <h1 class="display-6 mb-4">Search Results</h1>
        <p class="text-muted">Showing results for <strong>"{{ searchQuery }}"</strong> in <strong>{{ searchType.replace('-', ' ') }}</strong></p>

        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>

        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Searching...</p>
        </div>

        <div v-else-if="searchResults.length === 0" class="alert alert-info text-center py-5">
            <h5>No Results Found</h5>
            <p class="mb-0">No matches found for "{{ searchQuery }}" in {{ searchType.replace('-', ' ') }}.</p>
        </div>

        <div v-else class="row g-4">
            <template v-if="searchType === 'applications'">
                <div v-for="item in searchResults" :key="item.id" class="col-md-6 col-lg-4">
                    <div class="card h-100 shadow-sm border-0">
                        <div class="card-body">
                            <h5 class="card-title text-primary">Application #{{ item.id }}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">{{ item.student_name || 'Unknown Student' }}</h6>
                            <p class="card-text mb-1"><small><strong>Role:</strong> {{ item.job_title }}</small></p>
                            <p class="card-text mb-1"><small><strong>Status:</strong> 
                                <span :class="{
                                    'text-success': item.status === 'accepted',
                                    'text-danger': item.status === 'rejected',
                                    'text-warning': item.status === 'pending'
                                }">{{ item.status }}</span>
                            </small></p>
                        </div>
                        <div class="card-footer bg-white border-0 text-end">
                            <router-link :to="`/application/${item.id}`" class="btn btn-sm btn-outline-info">View Details</router-link>
                        </div>
                    </div>
                </div>
            </template>

            <template v-else-if="searchType === 'placement-drives'">
                <div v-for="item in searchResults" :key="item.id" class="col-md-6 col-lg-4">
                    <div class="card h-100 shadow-sm border-0">
                        <div class="card-body">
                            <h5 class="card-title text-primary">{{ item.job_title }}</h5>
                            <p class="card-text mb-1"><small><strong>Salary:</strong> ₹{{ item.salary }}</small></p>
                            <p class="card-text mb-1"><small><strong>Deadline:</strong> {{ item.deadline }}</small></p>
                            <p class="card-text mb-1"><small><strong>Status:</strong> {{ item.status }}</small></p>
                        </div>
                        <div class="card-footer bg-white border-0 text-end">
                            <router-link :to="`/placement-drive/${item.id}`" class="btn btn-sm btn-outline-info">View Details</router-link>
                        </div>
                    </div>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped>
.card {
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.card:hover {
    transform: translateY(-3px);
    box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
}
</style>
