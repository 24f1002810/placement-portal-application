<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/services/api";
import { useRouter, useRoute } from "vue-router";
import { useStore } from "vuex";
import Edit_company from "./edit_company.vue";

const router = useRouter();
const route = useRoute();
const store = useStore();
const loading = ref(true);
const error = ref("");
const drives = ref([]);
const searchQuery = ref("");
const sortBy = ref("job_title");
const sortOrder = ref("asc");
const filterStatus = ref("all");
const filterSalary = ref(0);

const companyId = computed(() => {
  if (route.params.id) {
    return route.params.id;
  }
  const role = store.getters["user/getUserRole"];
  if (role === "company") {
    return store.getters["user/getCompanyId"];
  }
  return null;
});
const isCompanyView = computed(() => !!companyId.value);

onMounted(async () => {
  await fetchDrives();
});

const fetchDrives = async () => {
  loading.value = true;
  error.value = "";

  try {
    let response;
    if (isCompanyView.value) {
      response = await api.get(`api/company/${companyId.value}/placement-drives`);
    } else {
      response = await api.get("api/admin/placement-drives");
    }
    drives.value = response.data.placement_drives;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load placement drives";
    console.error("Drives list error:", err);
  } finally {
    loading.value = false;
  }
};

const filteredAndSortedDrives = () => {
  let filtered = drives.value.filter((drive) => {
    const query = searchQuery.value.toLowerCase();
    const matchesSearch =
      drive.job_title.toLowerCase().includes(query) ||
      drive.company_name.toLowerCase().includes(query);

    const matchesStatus =
      filterStatus.value === "all" || drive.status === filterStatus.value;
    const matchesSalary = drive.salary >= filterSalary.value;

    return matchesSearch && matchesStatus && matchesSalary;
  });

  filtered.sort((a, b) => {
    let aVal = a[sortBy.value];
    let bVal = b[sortBy.value];

    if (typeof aVal === "string") {
      aVal = aVal.toLowerCase();
      bVal = bVal.toLowerCase();
    }

    if (aVal < bVal) return sortOrder.value === "asc" ? -1 : 1;
    if (aVal > bVal) return sortOrder.value === "asc" ? 1 : -1;
    return 0;
  });

  return filtered;
};

const toggleSort = (field) => {
  if (sortBy.value === field) {
    sortOrder.value = sortOrder.value === "asc" ? "desc" : "asc";
  } else {
    sortBy.value = field;
    sortOrder.value = "asc";
  }
};

const getSortIcon = (field) => {
  if (sortBy.value !== field) return "↕️";
  return sortOrder.value === "asc" ? "↑" : "↓";
};

const getStatusBadgeClass = (status) => {
  if (status === "approved") return "bg-success";
  if (status === "closed") return "bg-warning text-dark";
  if (status === "rejected") return "bg-danger";
  return "bg-secondary";
};

const getDeadlineClass = (deadline) => {
  const today = new Date();
  const deadlineDate = new Date(deadline);
  const daysLeft = Math.floor((deadlineDate - today) / (1000 * 60 * 60 * 24));

  if (daysLeft < 0) return "text-danger fw-bold";
  if (daysLeft < 7) return "text-warning fw-bold";
  return "text-success";
};

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
};

const viewDriveDetails = (driveId) => {
  router.push(`/placement-drive/${driveId}`);
};

const getActiveCount = () => {
  return drives.value.filter((d) => d.status === "approved").length;
};

const getClosedCount = () => {
  return drives.value.filter((d) => d.status === "closed").length;
};

const getRejectedCount = () => {
  return drives.value.filter((d) => d.status === "rejected").length;
};


const editDrive = (driveId) => {
  router.push(`/placement-drive/${driveId}/edit`);
}

function deleteDrive(driveId) {
  if (confirm("Are you sure you want to delete this drive?")) {
    api.delete(`api/placement-drive/${driveId}`)
      .then((response) => {
        alert(response.data.message || "Drive deleted successfully.");
        fetchDrives();
      }).catch((err) => {
        console.error("Error deleting drive:", err);
        alert("Failed to delete the drive.");
      });
  }
}

</script>

<template>
  <div class="container-fluid mt-5 mb-5">
    <!-- Header Section -->
    <div class="row mb-4">
      <div class="col">
        <h1 class="display-5">
          {{ isCompanyView ? "Company Placement Drives" : "Placement Drives" }}
        </h1>
        <p class="text-muted">
          {{
            isCompanyView
              ? "View placement drives for this company"
              : "Manage and view all placement drives"
          }}
        </p>
      </div>
      <div class="col-auto">
        <div class="d-flex gap-3">
          <button
            v-if="isCompanyView"
            @click="router.back()"
            class="btn btn-outline-secondary"
            title="Back to Company Details"
          >
            ← Back
          </button>
          <div class="badge bg-primary text-white p-3" v-if="!loading">
            <h6 class="mb-0">Total: {{ drives.length }}</h6>
          </div>
          <div class="badge bg-success text-white p-3" v-if="!loading">
            <h6 class="mb-0">Active: {{ getActiveCount() }}</h6>
          </div>
          <div class="badge bg-warning text-dark p-3" v-if="!loading">
            <h6 class="mb-0">Closed: {{ getClosedCount() }}</h6>
          </div>
          <div class="badge bg-danger text-white p-3" v-if="!loading">
            <h6 class="mb-0">Rejected: {{ getRejectedCount() }}</h6>
          </div>
        </div>
      </div>
    </div>

    <!-- Error Alert -->
    <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
      {{ error }}
      <button
        type="button"
        class="btn-close"
        data-bs-dismiss="alert"
        aria-label="Close"
      ></button>
    </div>

    <!-- Search and Filters -->
    <div class="card mb-4">
      <div class="card-body">
        <div class="row g-3">
          <div class="col-lg-5">
            <label class="form-label">Search Drives</label>
            <input
              v-model="searchQuery"
              type="text"
              class="form-control form-control-lg"
              placeholder="Search by job title or company name..."
            />
          </div>
          <div class="col-lg-2">
            <label class="form-label">Status</label>
            <select v-model="filterStatus" class="form-select form-select-lg">
              <option value="all">All Status</option>
              <option value="approved">Approved</option>
              <option value="closed">Closed</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading placement drives...</p>
    </div>

    <!-- Drives Table -->
    <div v-else-if="filteredAndSortedDrives().length > 0" class="card">
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th class="cursor-pointer" @click="toggleSort('id')" style="width: 60px">
                ID {{ getSortIcon("id") }}
              </th>
              <th class="cursor-pointer" @click="toggleSort('job_title')">
                Job Title {{ getSortIcon("job_title") }}
              </th>
              <th class="cursor-pointer" @click="toggleSort('company_name')">
                Company {{ getSortIcon("company_name") }}
              </th>
              <th class="cursor-pointer" @click="toggleSort('deadline')">
                Deadline {{ getSortIcon("deadline") }}
              </th>
              <th class="cursor-pointer" @click="toggleSort('status')">
                Status {{ getSortIcon("status") }}
              </th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="drive in filteredAndSortedDrives()" :key="drive.id">
              <td class="fw-bold">{{ drive.id }}</td>
              <td>
                <div class="fw-bold">{{ drive.job_title }}</div>
                <small class="text-muted">{{ drive.skills_required }}</small>
              </td>
              <td class="fw-bold">{{ drive.company_name }}</td>
              <td :class="getDeadlineClass(drive.deadline)">
                {{ formatDate(drive.deadline) }}
              </td>
              <td>
                <span :class="['badge', getStatusBadgeClass(drive.status)]">
                  {{ drive.status.charAt(0).toUpperCase() + drive.status.slice(1) }}
                </span>
              </td>
              <td class="align-center text-center">
                <button
                  @click="viewDriveDetails(drive.id)"
                  class="btn btn-sm btn-outline-primary me-2"
                  title="View Details"
                >
                  View 
                </button>
                <button class="btn btn-sm btn-info me-2" title="Edit Drive" @click="editDrive(drive.id)">
                  Edit
                </button>
                <button class="btn btn-sm btn-danger me-2" title="Delete Drive" @click="deleteDrive(drive.id)">
                  Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer text-muted text-center">
        Showing {{ filteredAndSortedDrives().length }} of {{ drives.length }} placement
        drives
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="card text-center py-5">
      <div class="card-body">
        <h5 class="card-title">
          {{ isCompanyView ? "No Drives Posted" : "No Drives Found" }}
        </h5>
        <p class="card-text text-muted">
          {{
            isCompanyView
              ? "This company has not posted any placement drives yet."
              : "No placement drives match your search criteria."
          }}
        </p>
        <button
          @click="
            searchQuery = '';
            filterStatus = 'all';
            filterSalary = 0;
          "
          class="btn btn-outline-primary"
        >
          Clear Filters
        </button>
        <button
          v-if="isCompanyView"
          @click="router.back()"
          class="btn btn-outline-secondary ms-2"
        >
          Back to Company
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
  user-select: none;
}

.cursor-pointer:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

.table-responsive {
  max-height: 800px;
}
</style>
