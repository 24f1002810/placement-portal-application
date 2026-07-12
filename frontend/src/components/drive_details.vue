<script setup>
import { ref, onMounted, computed } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useStore } from "vuex";
import api from "@/services/api";

const route = useRoute();
const router = useRouter();
const store = useStore();
const loading = ref(true);
const error = ref("");
const drive = ref(null);

const userRole = computed(() => store.getters['user/getUserRole']);
const isAdmin = computed(() => userRole.value === 'admin');
const isCompany = computed(() => userRole.value === 'company');
const isStudent = computed(() => userRole.value === 'student');
const canEditDrive = computed(() => isAdmin.value || isCompany.value);

const studentId = computed(() => store.getters['user/getStudentId']);

const updateDriveStatus = async (driveId, status) => {
  if (confirm(`Are you sure you want to change the status to ${status}?`)) {
    loading.value = true;
    try {
      const response = await api.post(`api/placement-drive/${driveId}`, { status: status });
      drive.value.status = status;
      if (status === 'rejected') {
        router.push({ name: "DriveList" });
      } else {
        alert(response.data.message || `Drive status updated to ${status}`);
      }
    } catch (err) {
      error.value = err.response?.data?.message || `Failed to update drive status`;
      console.error(`Error updating drive status:`, err);
    } finally {
      loading.value = false;
    }
  }
};

onMounted(async () => {
  try {
    const driveId = route.params.id;
    const response = await api.get(`api/placement-drive/${driveId}`);
    drive.value = response.data.drive;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load drive details";
    console.error("Drive details error:", err);
  } finally {
    loading.value = false;
  }
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const getStatusBadgeClass = (status) => {
  switch (status) {
    case "approved":
      return "bg-success";
    case "pending":
      return "bg-warning";
    case "rejected":
      return "bg-danger";
    default:
      return "bg-secondary";
  }
};

const editDrive = (driveId) => {
  router.push(`/placement-drive/${driveId}/edit`);
}

async function applyToDrive(driveId) {
  if (confirm("Are you sure you want to apply for this drive?")){
    const res= await api.post(`/api/placement-drive/${driveId}/apply`);
    if(res.status === 200){
      alert("Applied successfully");
      router.back();
    }else{
      alert("Failed to apply");
    }
  }
}
</script>

<template>
  <div class="container mt-5 mb-5">
    <div v-if="loading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div
      v-else-if="error"
      class="alert alert-danger alert-dismissible fade show"
      role="alert"
    >
      {{ error }}
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
      ></button>
    </div>

    <div v-if="isStudent && drive?.has_applied" class="alert alert-success mt-3" role="alert">
      You have successfully applied for this placement drive. 
      <router-link :to="`/application/${drive.application_id}`" class="alert-link">View Application</router-link>
    </div>

    <div v-else-if="drive" class="row">
      <div class="col-lg-8">
        <!-- Drive Header Card -->
        <div class="card mb-4">
          <div class="card-header bg-primary text-white">
            <div class="row align-items-center">
              <div class="col">
                <h2 class="mb-0">{{ drive.job_title }}</h2>
                <p class="mb-0 mt-2 text-light">{{ drive.company_name }}</p>
              </div>
              <div class="col-auto">
                <span :class="['badge', 'fs-6', getStatusBadgeClass(drive.status)]">
                  {{ drive.status?.toUpperCase() }}
                </span>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <h6 class="text-muted">Drive ID</h6>
                <p class="fs-6">{{ drive.id }}</p>
              </div>
              <div class="col-md-6">
                <h6 class="text-muted">Company ID</h6>
                <p class="fs-6">{{ drive.company_id }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Job Information Card -->
        <div class="card mb-4">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Job Information</h5>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <h6 class="text-muted">Job Title</h6>
              <p class="fs-6">{{ drive.job_title }}</p>
            </div>
            <div>
              <h6 class="text-muted">Job Description</h6>
              <p class="fs-6">{{ drive.job_description || "N/A" }}</p>
            </div>
          </div>
        </div>

        <!-- Requirements Card -->
        <div class="card mb-4">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Requirements</h5>
          </div>
          <div class="card-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <h6 class="text-muted">Skills Required</h6>
                <p class="fs-6">{{ drive.skills_required || "N/A" }}</p>
              </div>
              <div class="col-md-6">
                <h6 class="text-muted">Minimum CGPA</h6>
                <p class="fs-6">{{ drive.min_cgpa || "N/A" }}</p>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <h6 class="text-muted">Work Experience Required (Years)</h6>
                <p class="fs-6">{{ drive.working_experience_required || 0 }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Compensation & Timeline Card -->
        <div class="card mb-4">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Compensation & Timeline</h5>
          </div>
          <div class="card-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <h6 class="text-muted">Salary Package</h6>
                <p class="fs-6">
                  <strong>₹{{ drive.salary?.toLocaleString() || "N/A" }}</strong>
                </p>
              </div>
              <div class="col-md-6">
                <h6 class="text-muted">Application Deadline</h6>
                <p class="fs-6">{{ formatDate(drive.deadline) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Applicants Card -->
        <div class="card mb-4">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Applicants</h5>
          </div>
          <div class="card-body">
            <div class="text-center">
              <h3 class="display-4 text-primary">{{ drive.applicant_count }}</h3>
              <p class="text-muted">Total Applicants</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="col-lg-4">
        <!-- Quick Actions Card -->
        <div class="card sticky-top mb-3">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Quick Actions</h5>
          </div>
          <div class="card-body d-grid gap-2">
            <button class="btn btn-outline-primary" v-if="canEditDrive" @click="editDrive(drive.id)">
              Edit Drive
            </button>
            
            <button v-if="drive.status === 'approved'"  class="btn btn-outline-info">
              <router-link :to="`/applications?drive_id=${drive.id}`">
                View Applicants
              </router-link>
            </button>
            
            <button
              v-if="drive.status !== 'approved' && isAdmin"
              class="btn btn-outline-success"
              @click="updateDriveStatus(drive.id, 'approved')"
            >
              Approve Drive
            </button>
            <button
              v-if="canEditDrive && isAdmin"
              class="btn btn-outline-danger"
              @click="updateDriveStatus(drive.id, 'rejected')"
            >
              Reject Drive
            </button>
            <button class="btn btn-outline-danger" v-if="canEditDrive && drive.status == 'approved' && isCompany"
            @click="updateDriveStatus(drive.id, 'closed')">
              End Drive
            </button>
            <router-link
              :to="`/company/${drive.company_id}`"
              class="btn btn-outline-info mt-3 w-100"
              v-if="!isCompany"
              >View Company Details
            </router-link>
            <button v-if="isStudent && !drive.has_applied && drive.status === 'approved'" 
                    class="btn btn-outline-success mt-3 w-100" 
                    @click="applyToDrive(drive.id)">
              Apply
            </button>
            <router-link v-if="isStudent && drive.has_applied" 
                         :to="`/application/${drive.application_id}`" 
                         class="btn btn-outline-primary mt-3 w-100">
              View Your Application
            </router-link>
            
          </div>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-info text-center">No drive data available</div>
  </div>
</template>

<style scoped>
.card {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: none;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.125);
}

h6.text-muted {
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.fs-6 {
  word-break: break-word;
}

.sticky-top {
  top: 20px;
}

.badge {
  font-size: 0.9rem;
  padding: 0.5rem 0.75rem;
}

.btn {
  font-weight: 500;
  padding: 0.6rem 1rem;
}

.display-4 {
  font-weight: bold;
  color: #0d6efd;
}

.d-grid.gap-2 > * + * {
  margin-top: 0.5rem;
}

.d-grid.gap-3 > * + * {
  margin-top: 0.75rem;
}
</style>
