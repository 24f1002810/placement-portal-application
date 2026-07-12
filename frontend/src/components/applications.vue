<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/services/api";
import { useRoute } from "vue-router";
import { useStore } from "vuex";

const route = useRoute();
const store = useStore();

const applications = ref([]);
const loading = ref(true);
const error = ref("");
const statusFilter = ref("all");
const driveId = ref(route.query.drive_id || null);
let message = ref('')

const role = store.getters['user/getUserRole'];

onMounted(async () => {
  if (driveId.value) {
    statusFilter.value = "applied";
  }
  await fetchApplications();
});

const fetchApplications = async () => {
  try {
    const isAdmin = store.getters['user/isAdmin'];
    let url = "/api/admin/applications";
    
    if (!isAdmin) {
      const companyId = route.params.id;
      if (companyId) {
        url = `/api/company/${companyId}/applications`;
      }
    }
    
    const response = await api.get(url);
    applications.value = response.data.applications;
  } catch (err) {
    error.value = "Failed to load applications.";
    console.error("Error fetching applications:", err);
  } finally {
    loading.value = false;
  }
};

const filteredApplications = computed(() => {
  let filtered = applications.value;
  
  if (driveId.value) {
    filtered = filtered.filter(app => app.drive_id == driveId.value);
  }
  
  if (statusFilter.value !== "all") {
    filtered = filtered.filter(app => app.status === statusFilter.value);
  }
  
  return filtered;
});

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  return date.toLocaleDateString();
};

const getStatusBadgeClass = (status) => {
  const s = status.toLowerCase();
  if (s === 'applied') return 'badge bg-primary';
  if (s === 'shortlisted') return 'badge bg-info text-dark';
  if (s === 'selected (for interview)') return 'badge bg-warning text-dark';
  if (s === 'offered' || s === 'placed') return 'badge bg-success';
  if (s === 'rejected') return 'badge bg-danger';
  return 'badge bg-secondary';
};

const deleteApplication = async (id) => {
  if (confirm("Do you want to delete this application?")){
    loading.value = true;
    try {
      const response = await api.delete(`api/application/${id}`);
      message.value = response.data.message;
      fetchApplications();
    } catch (err) {
      error.value = "Failed to delete application.";
      console.error("Error deleting application:", err);
    } finally {
      loading.value = false;
    }
  }
}

async function rejectApplication(id){
  if (confirm(`Do you want to reject application ${id}?`)){
    try {
      const response = await api.post(`api/application/${id}`, {"status" : "rejected"});
      message.value = response.data.message;
      fetchApplications();
    } catch (err) {
      error.value = "Failed to reject application.";
      console.error("Error rejecting application:", err);
    } finally {
      loading.value = false;
    }
  }
}
</script>

<template>
  <div class="container mt-4">
    <div v-if="message" class="alert alert-success" role="alert">
      {{ message }}
    </div>
    <div v-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Student Applications</h2>
      <div class="d-flex align-items-center">
        <label for="statusFilter" class="me-2 fw-bold">Filter by Status:</label>
        <select id="statusFilter" v-model="statusFilter" class="form-select w-auto">
          <option value="all">All</option>
          <option value="applied">Applied</option>
          <option value="shortlisted">Shortlisted</option>
          <option value="selected (for interview)">Selected (for interview)</option>
          <option value="offered">Offered</option>
          <option value="placed">Placed</option>
          <option value="rejected">Rejected</option>
        </select>
      </div>
    </div>

    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <table class="table table-hover table-striped mb-0">
            <thead class="table-dark text-center">
              <tr>
                <th>ID</th>
                <th>Student Name</th>
                <th v-if="role === 'admin'">Company</th>
                <th>Job Title</th>
                <th>Date Applied</th>
                <th>Interview Date</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody class="text-center">
              <tr v-for="app in filteredApplications" :key="app.id">
                <td>{{ app.id }}</td>
                <td>{{ app.student_name }}</td>
                <td v-if="role === 'admin'">{{ app.company_name }}</td>
                <td>{{ app.job_title }}</td>
                <td>{{ formatDate(app.date) }}</td>
                <td>{{ formatDate(app.interview_date) }}</td>
                <td>
                  <span :class="getStatusBadgeClass(app.status) + ' text-capitalize'">
                    {{ app.status }}
                  </span>
                </td>
                <td>
                    <router-link :to="`/application/${app.id}`" class="btn btn-sm btn-outline-primary me-2" title="View Application">
                      View 
                    </router-link>
                    <button v-if="role === 'admin'" class="btn btn-sm btn-outline-danger me-2" title="Delete Application" @click="deleteApplication(app.id)">
                      Delete
                    </button>
                    <button v-if="role === 'company' && app.status !== 'rejected' && app.status !== 'placed'"
                     class="btn btn-sm btn-outline-danger me-2" title="Reject Application" 
                     @click="rejectApplication(app.id)">
                      Reject
                    </button>
                </td>
              </tr>
              <tr v-if="filteredApplications.length === 0">
                <td colspan="6" class="text-center py-4 text-muted">
                  No applications found for the selected status.
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
</style>
