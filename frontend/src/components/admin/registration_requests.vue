<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";

const message = ref("");
const loading = ref(true);
const error = ref("");
const companies = ref(null);

onMounted(async () => {
  try {
    const response = await api.get("/api/registration-requests");
    companies.value = response.data.pending_companies;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load dashboard";
    console.error("Dashboard error:", err);
  } finally {
    loading.value = false;
  }
});

const requestStatusUpdate = async (requestId, action) => {
  if (confirm(`Are you sure you want to ${action} this company?`)){
    loading.value = true;
    error.value = "";
    try {
      const response = await api.post(`/api/registration-requests`, {
        company_id: requestId,
        action: action,
      });
      message.value = response.data.message;
    } catch (err) {
      error.value = err.response?.data?.message;
      message.value = "";
      console.error("Update error:", err);
    }
  }
}
</script>
<template>
  <div class="container">
    <h2 class="text-center">Registration Requests</h2>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-alert alert-dismissible fade show" role="alert">
      {{ error }}
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
      ></button>
    </div>
    <div
      v-else-if="message"
      class="alert alert-success alert-dismissible fade show"
      role="alert"
    >
      {{ message }}
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
      ></button>
    </div>

    <div v-if="companies && companies.length === 0" class="alert alert-info text-center">
      No registration requests are pending
    </div>
    <div v-else>
      <table class="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Location</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="company in companies" :key="company.id">
            <td>{{ company.id }}</td>
            <td>{{ company.name }}</td>
            <td>{{ company.location }}</td>
            <td>
              <button class="btn btn-success btn-sm" @click="requestStatusUpdate(company.id, 'approve')">
                Approve
              </button>
              <button class="btn btn-danger btn-sm" @click="requestStatusUpdate(company.id, 'reject')">
                Reject
              </button>
              <button
                class="btn btn-secondary btn-sm"
                @click="$router.push(`/company/${company.id}/profile`)"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
<style scoped></style>
