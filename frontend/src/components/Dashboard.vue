<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";

const message = ref("");
const loading = ref(true);
const error = ref("");
const profile = ref(null);

onMounted(async () => {
  try {
    const response = await api.post("/api/dashboard");
    message.value = response.data.message;
    profile.value = response.data.profile;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load dashboard";
    console.error("Dashboard error:", err);
  } finally {
    loading.value = false;
  }
});
</script>
<template>
  <div class="dashboard-container">
    <h1>Dashboard</h1>
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-alert">{{ error }}</div>
    <div v-else class="message-box">
      <p>{{ message }}</p>
      <div v-if="profile" class="profile-info">
        <h2>{{ profile.name }}</h2>
        <p><strong>Email:</strong> {{ profile.email }}</p>
        <p><strong>Roles:</strong> {{ profile.roles.join(", ") }}</p>
        <div v-if="profile.skills && profile.skills.length">
          <p>
            <strong>Skills:</strong>
            {{
              Array.isArray(profile.skills) ? profile.skills.join(", ") : profile.skills
            }}
          </p>
        </div>
        <div v-if="profile.applications">
          <h3>Applications:</h3>
          <ul>
            <li v-for="app in profile.applications" :key="app.id">
              Drive ID: {{ app.drive_id }}, Date: {{ app.date }}, Status: {{ app.status }}
            </li>
          </ul>
        </div>
        <div v-if="profile.description">
          <p><strong>Description:</strong> {{ profile.description }}</p>
        </div>
        <div v-if="profile.industry">
          <p><strong>Industry:</strong> {{ profile.industry }}</p>
        </div>
        <div v-if="profile.drives">
          <p><strong>Placement Drives:</strong> {{ profile.drives.length }}</p>
        </div>
      </div>
    </div>
  </div>
</template>
<style scoped>
.dashboard-container {
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #1f2937;
  margin-bottom: 2rem;
}

.message-box {
  background-color: #dbeafe;
  color: #1e40af;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 1.1rem;
}

.loading {
  color: #6b7280;
  font-size: 1rem;
  margin-top: 1rem;
}

.error-alert {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}
.profile-info {
  margin-top: 1.5rem;
  text-align: left;
  display: inline-block;
  background-color: #f3f4f6;
  padding: 1rem;
  border-radius: 4px;
}
</style>
