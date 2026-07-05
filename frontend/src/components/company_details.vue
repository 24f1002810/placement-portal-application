<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const error = ref("");
const company = ref(null);

onMounted(async () => {
  try {
    const companyId = route.params.id;
    const response = await api.get(`api/company/${companyId}`);
    company.value = response.data.company;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load company details";
    console.error("Company details error:", err);
  } finally {
    loading.value = false;
  }
});

function viewPlacementDrives() {
  if (company.value && company.value.id) {
    // Navigate using Vue Router instead of window.location.href
    router.push({
      name: "CompanyDriveList",
      params: { id: company.value.id },
    });
  } else {
    console.error("Company ID is not available.");
  }
}

function deleteCompany() {
  if (confirm("Are you sure you want to delete this company?")) {
    api
      .delete(`api/company/${company.value.id}`)
      .then((response) => {
        alert(response.data.message || "Company deleted successfully.");
        router.push({ name: "CompanyList" });
      })
      .catch((err) => {
        console.error("Error deleting company:", err);
        alert("Failed to delete the company.");
      });
  }
}

function Edit_company() {
  router.push({ name: "EditCompany", params: { id: company.value.id } });
}
</script>

<template>
  <div class="container mt-5">
    <router-view v-if="$route.name === 'EditCompany'" />

    <template v-else>
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

      <div v-else-if="company" class="row">
        <div class="col-md-8">
          <!-- Company Header Card -->
          <div class="card mb-4">
            <div class="card-header bg-primary text-white">
              <h2 class="mb-0">{{ company.name }}</h2>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6 class="text-muted">Company ID</h6>
                  <p class="fs-6">{{ company.id }}</p>
                </div>
                <div class="col-md-6">
                  <h6 class="text-muted">Status</h6>
                  <p class="fs-6">
                    <span
                      :class="[
                        'badge',
                        company.approval_status === 'approved'
                          ? 'bg-success'
                          : company.approval_status === 'rejected'
                          ? 'bg-danger'
                          : 'bg-warning',
                      ]"
                    >
                      {{ company.approval_status }}
                    </span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Basic Information Card -->
          <div class="card mb-4">
            <div class="card-header bg-secondary text-white">
              <h5 class="mb-0">Basic Information</h5>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6 class="text-muted">Company Name</h6>
                  <p class="fs-6">{{ company.name }}</p>
                </div>
                <div class="col-md-6">
                  <h6 class="text-muted">Location</h6>
                  <p class="fs-6">{{ company.location }}</p>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6 class="text-muted">Industry</h6>
                  <p class="fs-6">{{ company.industry || "N/A" }}</p>
                </div>
                <div class="col-md-6">
                  <h6 class="text-muted">Website</h6>
                  <p class="fs-6">
                    <a v-if="company.website" :href="company.website" target="_blank">
                      {{ company.website }}
                    </a>
                    <span v-else>N/A</span>
                  </p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-12">
                  <h6 class="text-muted">Description</h6>
                  <p class="fs-6">{{ company.description || "N/A" }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Information Card -->
          <div class="card mb-4">
            <div class="card-header bg-secondary text-white">
              <h5 class="mb-0">Contact Information</h5>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6 class="text-muted">Contact Person</h6>
                  <p class="fs-6">HR</p>
                </div>
                <div class="col-md-6">
                  <h6 class="text-muted">Email</h6>
                  <p class="fs-6">
                    <a v-if="company.email" :href="`mailto:${company.email}`">
                      {{ company.email }}
                    </a>
                    <span v-else>N/A</span>
                  </p>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6">
                  <h6 class="text-muted">Phone</h6>
                  <p class="fs-6">
                    <a v-if="company.hr_phone" :href="`tel:${company.hr_phone}`">
                      {{ company.hr_phone }}
                    </a>
                    <span v-else>N/A</span>
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- Additional Information Card -->
          <div class="card mb-4">
            <div class="card-header bg-secondary text-white">
              <h5 class="mb-0">Additional Information</h5>
            </div>
            <div class="card-body">
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6 class="text-muted">Company Size</h6>
                  <p class="fs-6">{{ company.company_size || "N/A" }}</p>
                </div>
                <div class="col-md-6">
                  <h6 class="text-muted">Founded Year</h6>
                  <p class="fs-6">{{ company.founded_year || "N/A" }}</p>
                </div>
              </div>
              <div class="row mb-3">
                <div class="col-md-6">
                  <h6 class="text-muted">Registration Date</h6>
                  <p class="fs-6">
                    {{
                      company.created_at
                        ? new Date(company.created_at).toLocaleDateString()
                        : "N/A"
                    }}
                  </p>
                </div>
                <div class="col-md-6">
                  <h6 class="text-muted">Last Updated</h6>
                  <p class="fs-6">
                    {{
                      company.updated_at
                        ? new Date(company.updated_at).toLocaleDateString()
                        : "N/A"
                    }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="col-md-4">
          <div class="card sticky-top">
            <div class="card-header bg-info text-white">
              <h5 class="mb-0">Quick Actions</h5>
            </div>
            <div class="card-body">
              <button class="btn btn-primary w-100 mb-2" @click="Edit_company">
                Edit Company
              </button>
              <button class="btn btn-warning w-100 mb-2" @click="viewPlacementDrives">
                View Placement Drives
              </button>
              <button class="btn btn-danger w-100" @click="deleteCompany">
                Delete Company
              </button>
            </div>
          </div>

          <!-- Status Card -->
          <div class="card mt-3">
            <div class="card-header bg-light">
              <h6 class="mb-0">Status Summary</h6>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <div class="p-2 border rounded text-center">
                  <h6 class="text-muted">Approval Status</h6>
                  <span
                    :class="[
                      'badge fs-6',
                      company.approval_status === 'approved'
                        ? 'bg-success'
                        : company.approval_status === 'rejected'
                        ? 'bg-danger'
                        : 'bg-warning',
                    ]"
                  >
                    {{ company.approval_status?.toUpperCase() }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="alert alert-info text-center">No company data available</div>
    </template>
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
</style>
