<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/services/api";

const message = ref("");
const loading = ref(true);
const error = ref("");
const profile = ref(null);

const pendingCompanyRegistrations = computed(() => {
  return profile.value?.companies?.filter(c => c.approval_status === 'pending').length || 0;
});

const pendingPlacementDrives = computed(() => {
  return profile.value?.drives?.filter(d => d.status === 'pending').length || 0;
});

onMounted(async () => {
  try {
    const response = await api.post("/api/dashboard");
    message.value = response.data.message;
    profile.value = response.data.profile;
    console.log(message.value)
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load dashboard";
    console.error("Dashboard error:", err);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
    <div class="container">
    <div v-if="loading" class="loading">Loading...</div>
    <div v-else-if="error" class="error-alert">{{ error }}</div>
    <div v-else>
      <div v-if="profile">
        <div class="stats-row">
          <div class="stat-box">
            <div class="stat-number">{{ profile.students?.length || 0 }}</div>
            <div class="stat-label">Students</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{{ profile.companies?.length || 0 }}</div>
            <div class="stat-label">Companies</div>
          </div>
          <div class="stat-box">
            <div class="stat-number">{{ profile.drives?.length || 0 }}</div>
            <div class="stat-label">Placement Drives</div>
          </div>
        </div>

        <div class="row align-items-center gx-5">  
          <div class="col text-center">
            <button class="btn btn-primary btn-lg button-with-badge">
              Registration Requests
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {{ pendingCompanyRegistrations }}
                <span class="visually-hidden">unread messages</span>
              </span>
            </button>
          </div>
          <div class="col text-center">
            <button class="btn btn-primary btn-lg button-with-badge">
              Drive Requests
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                {{ pendingPlacementDrives }}
                <span class="visually-hidden">unread messages</span>
              </span>
            </button>
          </div>
        </div>
        
      </div>
    </div>
  </div>
</template>

<style scoped>

    h1 {
    text-align: center;
    color: #1f2937;
    margin-bottom: 2rem;
    }

    .stats-row {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
    justify-content: center;
    flex-wrap: wrap;
    }

    .stat-box {
    background-color: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 0.5rem;
    padding: 1.5rem;
    text-align: center;
    min-width: 200px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: box-shadow 0.3s ease, transform 0.3s ease;
    }

    .stat-box:hover {
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
    }

    .stat-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2563eb;
    margin-bottom: 0.5rem;
    }

    .stat-label {
    font-size: 1rem;
    color: #6b7280;
    font-weight: 500;
    }

    .profile-section {
    text-align: center;
    background-color: #f3f4f6;
    padding: 1.5rem;
    border-radius: 0.5rem;
    margin-top: 1rem;
    }

    .profile-section h2 {
    color: #1f2937;
    margin-bottom: 1rem;
    }

    .profile-section p {
    color: #374151;
    margin: 0.5rem 0;
    }

    .loading {
    color: #6b7280;
    font-size: 1rem;
    margin-top: 1rem;
    text-align: center;
    }

    .error-alert {
    background-color: #fee2e2;
    color: #b91c1c;
    padding: 1rem;
    border-radius: 4px;
    margin-top: 1rem;
    }

    .button-with-badge {
    position: relative;
    }
</style>
