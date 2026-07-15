<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api';

const loading = ref(true);
const error = ref(null);
const drives = ref([]);
const applications = ref([]);

onMounted(async () => {
  try {
    const response = await api.post('/api/dashboard');
    if (response.data && response.data.profile) {
      if (response.data.profile.drives) {
        drives.value = response.data.profile.drives;
      }
      const companyId = response.data.profile.company_id;
      if (companyId) {
        const appsResponse = await api.get(`/api/company/${companyId}/applications`);
        if (appsResponse.data && appsResponse.data.applications) {
          applications.value = appsResponse.data.applications;
        }
      }
    }
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load dashboard data";
    console.error("Dashboard error:", err);
  } finally {
    loading.value = false;
  }
});

const activeDrives = computed(() => {
  return drives.value.filter(drive => drive.status === 'approved');
});

const upcomingInterviewsThisMonth = computed(() => {
    const today = new Date();
    const currentMonth = today.getMonth();
    const currentYear = today.getFullYear();
    const startOfToday = new Date(today.getFullYear(), today.getMonth(), today.getDate());

    return applications.value.filter(app => {
        if (!app.interview_date) return false;
        const interviewDate = new Date(app.interview_date);
        return interviewDate >= startOfToday && 
               interviewDate.getMonth() === currentMonth && 
               interviewDate.getFullYear() === currentYear &&
               app.status !== 'rejected' && app.status !== 'placed';
    }).sort((a, b) => new Date(a.interview_date) - new Date(b.interview_date));
});
</script>

<template>
  <div class="container mt-4">

    <div v-if="upcomingInterviewsThisMonth.length > 0" class="mb-5">
      <h3 class="mb-4 fw-bold">Upcoming Interviews</h3>
      <div class="row">
        <div class="col-md-4 mb-4" v-for="app in upcomingInterviewsThisMonth" :key="'interview-' + app.id">
          <div class="card h-100 shadow-sm border-0 border-start border-warning border-4">
            <div class="card-body d-flex flex-column">
              <h5 class="card-title text-primary fw-bold">{{ app.job_title }}</h5>
              <h6 class="card-subtitle mb-3 text-muted">Candidate: {{ app.student_name }}</h6>
              <div class="mt-auto pt-3 border-top d-flex justify-content-between align-items-center">
                <span class="badge bg-warning text-dark px-3 py-2 rounded-pill">
                  <i class="bi bi-calendar-event me-1"></i>
                  {{ new Date(app.interview_date).toLocaleDateString() }}
                </span>
                <router-link 
                  :to="{ name: 'ApplicationDetail', params: { id: app.id }}" 
                  class="btn btn-outline-warning text-dark btn-sm fw-semibold">
                  View Application
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Active Placement Drives</h2>
      <router-link :to="{ name: 'CreateDrive' }" class="btn btn-primary">
        New Placement Drive
      </router-link>
    </div>
    
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
    
    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    
    <div v-else-if="activeDrives.length === 0" class="alert alert-info" role="alert">
      No active placement drives.
    </div>
    
    <div v-else class="row">
      <div class="col-md-4 mb-4" v-for="drive in activeDrives" :key="drive.id">
        <div class="card h-100 shadow-sm border-0">
          <div class="card-header bg-primary text-white">
            <h5 class="card-title mb-0">{{ drive.job_title }}</h5>
          </div>
          <div class="card-body d-flex flex-column">
            <p class="card-text text-muted mb-3">
              {{ drive.job_description.length > 100 ? drive.job_description.substring(0, 100) + '...' : drive.job_description }}
            </p>
            
            <ul class="list-group list-group-flush mb-3 flex-grow-1">
              <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
                Deadline
                <span class="badge bg-warning text-dark">{{ drive.deadline || 'N/A' }}</span>
              </li>
              <li class="list-group-item px-0 d-flex justify-content-between align-items-center">
                Min CGPA
                <span class="badge bg-secondary">{{ drive.min_cgpa }}</span>
              </li>
              <li class="list-group-item px-0 d-flex justify-content-between align-items-center border-bottom-0">
                Salary
                <span class="badge bg-success">₹{{ drive.salary }}</span>
              </li>
            </ul>
          </div>
          <div class="card-footer bg-light border-top-0 pt-0 pb-3">
            <div class="d-flex justify-content-between align-items-center mb-3">
              <span class="text-muted fw-bold">Applications:</span>
              <span class="badge rounded-pill bg-info text-dark fs-6 px-3 py-2">
                {{ drive.application_count }}
              </span>
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
              <router-link 
                :to="{ name: 'CompanyApplications', params: { id: $route.params.id }, query: { drive_id: drive.id } }" 
                class="btn btn-outline-primary btn-sm">
                Applications
              </router-link>
              <router-link 
                :to="{ name: 'DriveDetails', params: { id: drive.id } }" 
                class="btn btn-primary btn-sm">
                View Drive
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Using only Bootstrap for styling as requested */
.card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15) !important;
  transform: translateY(-0.5rem);
}
</style>
