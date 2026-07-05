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
const searchType = ref('students');

const fetchSearchResults = async () => {
    loading.value = true;
    error.value = '';
    searchResults.value = [];
    searchQuery.value = route.query.q || '';
    searchType.value = route.query.type || 'students';

    try {
        let response;
        let data = [];
        const query = searchQuery.value.toLowerCase();

        if (searchType.value === 'students') {
            response = await api.get('api/admin/students');
            data = response.data.students;
            
            searchResults.value = data.filter(student => 
                (student.name && student.name.toLowerCase().includes(query)) ||
                (student.email && student.email.toLowerCase().includes(query)) ||
                (student.phone_number && student.phone_number.includes(query))
            );
        } else if (searchType.value === 'companies') {
            response = await api.get('api/admin/companies');
            data = response.data.companies;

            searchResults.value = data.filter(company => 
                (company.name && company.name.toLowerCase().includes(query)) ||
                (company.industry && company.industry.toLowerCase().includes(query)) ||
                (company.location && company.location.toLowerCase().includes(query))
            );
        } else if (searchType.value === 'placement-drives') {
            response = await api.get('api/admin/placement-drives');
            data = response.data.placement_drives;

            searchResults.value = data.filter(drive => 
                (drive.job_title && drive.job_title.toLowerCase().includes(query)) ||
                (drive.company_name && drive.company_name.toLowerCase().includes(query)) ||
                (drive.skills_required && drive.skills_required.toLowerCase().includes(query))
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
        <p class="text-muted">Showing results for <strong>"{{ searchQuery }}"</strong> in <strong>{{ searchType }}</strong></p>

        <!-- Error Alert -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Searching...</p>
        </div>

        <!-- Empty State -->
        <div v-else-if="searchResults.length === 0" class="alert alert-info text-center py-5">
            <h5>No Results Found</h5>
            <p class="mb-0">No matches found for "{{ searchQuery }}" in {{ searchType }}.</p>
        </div>

        <!-- Results -->
        <div v-else class="row g-4">
            <template v-if="searchType === 'students'">
                <div v-for="item in searchResults" :key="item.id" class="col-md-6 col-lg-4">
                    <div class="card h-100 shadow-sm border-0">
                        <div class="card-body">
                            <h5 class="card-title text-primary">{{ item.name }}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">{{ item.email }}</h6>
                            <p class="card-text mb-1"><small><strong>Phone:</strong> {{ item.phone_number }}</small></p>
                            <p class="card-text mb-1"><small><strong>CGPA:</strong> <span class="badge bg-success">{{ item.cgpa }}</span></small></p>
                        </div>
                        <div class="card-footer bg-white border-0 text-end">
                            <router-link :to="`/student/${item.id}`" class="btn btn-sm btn-outline-info">View Details</router-link>
                        </div>
                    </div>
                </div>
            </template>

            <template v-else-if="searchType === 'companies'">
                <div v-for="item in searchResults" :key="item.id" class="col-md-6 col-lg-4">
                    <div class="card h-100 shadow-sm border-0">
                        <div class="card-body">
                            <h5 class="card-title text-primary">{{ item.name }}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">{{ item.industry || 'No Industry Specified' }}</h6>
                            <p class="card-text mb-1"><small><strong>Location:</strong> {{ item.location }}</small></p>
                            <p class="card-text mb-1"><small><strong>Status:</strong> 
                                <span :class="{'text-success': item.approval_status === 'approved', 'text-warning': item.approval_status === 'pending'}">{{ item.approval_status }}</span>
                            </small></p>
                        </div>
                        <div class="card-footer bg-white border-0 text-end">
                            <router-link :to="`/company/${item.id}`" class="btn btn-sm btn-outline-info">View Details</router-link>
                        </div>
                    </div>
                </div>
            </template>

            <template v-else-if="searchType === 'placement-drives'">
                <div v-for="item in searchResults" :key="item.id" class="col-md-6 col-lg-4">
                    <div class="card h-100 shadow-sm border-0">
                        <div class="card-body">
                            <h5 class="card-title text-primary">{{ item.job_title }}</h5>
                            <h6 class="card-subtitle mb-2 text-muted">{{ item.company_name }}</h6>
                            <p class="card-text mb-1"><small><strong>Salary:</strong> ₹{{ item.salary }}</small></p>
                            <p class="card-text mb-1"><small><strong>Deadline:</strong> {{ item.deadline }}</small></p>
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
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1) !important;
}
</style>