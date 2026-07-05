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

const userRoles = computed(() => store.getters["user/getUser"]?.roles || []);
const isAdmin = computed(() => store.getters["user/isAdmin"]);
const isCompany = computed(() => userRoles.value.includes("company"));
const canEditDrive = computed(() => isAdmin.value || isCompany.value);

const approveRequest = (requestId) => {
  // Implement API call to approve the registration request
  console.log("Approving request ID:", requestId);
  loading.value = true;
  error.value = "";
  api
    .post(`/api/drive-requests`, { drive_id: requestId, action: "approve" })
    .then((response) => {
      // Capture the success message from the API response
      message.value = response.data.message || "Request approved successfully";
      // Refresh the list of registration requests after approval
      return api.get("/api/drive-requests");
    })
    .then((response) => {
      drives.value = response.data.pending_drives;
    })
    .catch((err) => {
      error.value = err.response?.data?.message || "Failed to approve request";
      message.value = "";
      console.error("Approval error:", err);
    })
    .finally(() => {
      loading.value = false;
    });
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

function deleteDrive() {
  if (confirm("Are you sure you want to delete this drive?")) {
    // Call API to delete the drive
    api
      .delete(`api/placement-drive/${drive.value.id}`)
      .then((response) => {
        alert(response.data.message || "Drive deleted successfully.");
        // Redirect or update the UI as needed
        router.push({ name: "DriveList" }); // Assuming you have a route named 'AdminPlacementDrives'
      })
      .catch((err) => {
        console.error("Error deleting drive:", err);
        alert("Failed to delete the drive.");
      });
  }
}

const editDrive = (driveId) => {
  router.push(`/placement-drive/${driveId}/edit`);
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
            <button class="btn btn-outline-info">
              View Applicants
            </button>
            <button
              v-if="drive.status !== 'approved'"
              class="btn btn-outline-success"
              @click="approveRequest(drive.id)"
            >
              Approve Drive
            </button>
            <button
              v-if="canEditDrive"
              class="btn btn-outline-danger"
              @click="deleteDrive"
            >
              Delete Drive
            </button>
            <router-link
              :to="`/company/${drive.company_id}`"
              class="btn btn-outline-info mt-3 w-100"
              v-if="!isCompany"
              >View Company Details</router-link
            >
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
