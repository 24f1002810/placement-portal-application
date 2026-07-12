<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";
import { useRouter } from "vue-router";

const router = useRouter();
const loading = ref(true);
const error = ref("");
const companies = ref([]);
const searchQuery = ref("");
const sortBy = ref("name");
const sortOrder = ref("asc");
const filterStatus = ref("all");

onMounted(async () => {
    await fetchCompanies();
});

const fetchCompanies = async () => {
    loading.value = true;
    error.value = "";
    try {
        const response = await api.get("api/admin/companies");
        companies.value = response.data.companies;
    } catch (err) {
        error.value = err.response?.data?.message || "Failed to load companies";
        console.error("Companies list error:", err);
    } finally {
        loading.value = false;
    }
};

const filteredAndSortedCompanies = () => {
    let filtered = companies.value.filter(company => {
        const query = searchQuery.value.toLowerCase();
        const matchesSearch = 
            company.name.toLowerCase().includes(query) ||
            company.industry.toLowerCase().includes(query) ||
            company.location.toLowerCase().includes(query) ||
            company.email.toLowerCase().includes(query);
        
        const matchesStatus = filterStatus.value === "all" || company.approval_status === filterStatus.value;
        
        return matchesSearch && matchesStatus;
    });

    filtered.sort((a, b) => {
        let aVal = a[sortBy.value];
        let bVal = b[sortBy.value];

        if (typeof aVal === 'string') {
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
    if (status === 'approved') return "bg-success";
    if (status === 'pending') return "bg-warning text-dark";
    if (status === 'rejected') return "bg-danger";
    return "bg-secondary";
};

const viewCompanyDetails = (companyId) => {
    router.push({ name: "CompanyProfile", params: { id: companyId } });
};

const getApprovedCount = () => {
    return companies.value.filter(c => c.approval_status === 'approved').length;
};

const getPendingCount = () => {
    return companies.value.filter(c => c.approval_status === 'pending').length;
};


const editCompany = (companyId) => {
    router.push({name:'AdminEditCompany', params:{id:companyId}})
}

async function deleteCompany(companyId){
    if (confirm("Are you sure you want to delete this company?")) {
        api.delete(`api/company/${companyId}`)
        .then((response) => {
            alert(response.data.message || "Company deleted successfully!");
            fetchCompanies();
        })
        .catch(error => {
            alert("Failed to delete company");
            console.log("Error in deleting company: " + error);
        })
    }
}


const editCompanyStatus = async (companyId, action) => {
    if (confirm(`Are you sure you want to ${action} company ${companyId}?`)) {
        api.post('/api/registration-requests', {'company_id':companyId, 'action':action})
        .then((response) => {
            alert(response.data.message || `Company ${action} successfully`);
            fetchCompanies();
        })
        .catch((error) => {
            alert(`Failed to ${action} company`);
            console.log(`Error in ${action} company:`, error);
        })
    }
}


function updateBlockStatus(id, is_blocked) {
  if (id) {
    api
      .post(`api/company/${id}`, { 'block': is_blocked })
      .then((response) => {
        alert(response.data.message || "Company blocked status updated successfully.");
        const company = companies.value.find(c => c.id === id);
        if (company) {
          company.active = !is_blocked;
        }
      })
      .catch((err) => {
        console.error("Error updating company block status:", err);
        alert("Failed to update company block status.");
      });
  }
}

</script>

<template>
    <div class="container-fluid mt-5 mb-5">
        <!-- Header Section -->
        <div class="row mb-4">
            <div class="col">
                <h1 class="display-5">Registered Companies</h1>
                <p class="text-muted">Manage and view all company profiles</p>
            </div>
            <div class="col-auto">
                <div class="d-flex gap-3">
                    <div class="badge bg-primary text-white p-3" v-if="!loading">
                        <h6 class="mb-0">Total: {{ companies.length }}</h6>
                    </div>
                    <div class="badge bg-success text-white p-3" v-if="!loading">
                        <h6 class="mb-0">Approved: {{ getApprovedCount() }}</h6>
                    </div>
                    <div class="badge bg-warning text-dark p-3" v-if="!loading">
                        <h6 class="mb-0">Pending: {{ getPendingCount() }}</h6>
                    </div>
                </div>
            </div>
        </div>

        <!-- Error Alert -->
        <div v-if="error" class="alert alert-danger alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>

        <!-- Search and Filters -->
        <div class="card mb-4">
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-6">
                        <input
                            v-model="searchQuery"
                            type="text"
                            class="form-control form-control-lg"
                            placeholder="Search by company name, industry, location, or email..."
                        />
                    </div>
                    <div class="col-md-3">
                        <select v-model="filterStatus" class="form-select form-select-lg">
                            <option value="all">All Status</option>
                            <option value="approved">Approved</option>
                            <option value="pending">Pending</option>
                            <option value="rejected">Rejected</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <button 
                            @click="fetchCompanies"
                            class="btn btn-primary w-100 btn-lg"
                            :disabled="loading"
                        >
                            <span v-if="!loading">🔄 Refresh</span>
                            <span v-else>
                                <span class="spinner-border spinner-border-sm me-2"></span>
                                Loading...
                            </span>
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Loading State -->
        <div v-if="loading" class="text-center py-5">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
            <p class="mt-3 text-muted">Loading companies...</p>
        </div>

        <!-- Companies Table -->
        <div v-else-if="filteredAndSortedCompanies().length > 0" class="card">
            <div class="table-responsive">
                <table class="table table-hover mb-0">
                    <thead class="table-light">
                        <tr>
                            <th class="cursor-pointer" @click="toggleSort('id')">
                                ID {{ getSortIcon('id') }}
                            </th>
                            <th class="cursor-pointer" @click="toggleSort('name')">
                                Company Name {{ getSortIcon('name') }}
                            </th>
                            <th class="cursor-pointer" @click="toggleSort('industry')">
                                Industry {{ getSortIcon('industry') }}
                            </th>
                            <th class="cursor-pointer" @click="toggleSort('location')">
                                Location {{ getSortIcon('location') }}
                            </th>
                            <th class="cursor-pointer" @click="toggleSort('approval_status')">
                                Status {{ getSortIcon('approval_status') }}
                            </th>
                            <th class="text-center" style="min-width: 200px;">Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="company in filteredAndSortedCompanies()" :key="company.id">
                            <td class="fw-bold">{{ company.id }}</td>
                            <td class="fw-bold">
                                <div>{{ company.name }}</div>
                                <small class="text-muted">{{ company.website }}</small>
                            </td>
                            <td>{{ company.industry || 'N/A' }}</td>
                            <td>{{ company.location }}</td>
                            <td>
                                <span :class="['badge', getStatusBadgeClass(company.approval_status)]">
                                    {{ company.approval_status.charAt(0).toUpperCase() + company.approval_status.slice(1) }}
                                </span>
                            </td>
                            <td class="text-center">
                                <div class="d-flex justify-content-center gap-2">
                                    <button
                                        @click="viewCompanyDetails(company.id)"
                                        class="btn btn-sm btn-outline-primary"
                                        title="View Details"
                                    >
                                        View
                                    </button>
                                    <button
                                        class="btn btn-sm btn-warning"
                                        title="Edit"
                                        @click="editCompany(company.id)"
                                    >
                                        Edit
                                    </button>
                                    <button
                                        class="btn btn-sm btn-danger"
                                        title="Delete"
                                        @click="deleteCompany(company.id)"
                                    >
                                        Delete
                                    </button>
                                    
                                    <template v-if="company.approval_status === 'approved'">
                                        <button
                                            v-if="company.active"
                                            class="btn btn-sm btn-secondary"
                                            title="Block"
                                            @click="updateBlockStatus(company.id, true)"
                                        >
                                            Block
                                        </button>
                                        <button
                                            v-else
                                            class="btn btn-sm btn-success text-white"
                                            title="Unblock"
                                            @click="updateBlockStatus(company.id, false)"
                                        >
                                            Unblock
                                        </button>
                                    </template>
                                    <template v-else-if="company.approval_status === 'pending'">
                                        <button
                                            class="btn btn-sm btn-success"
                                            title="Approve"
                                            @click="editCompanyStatus(company.id, 'approve')"
                                        >
                                            Approve
                                        </button>
                                        <button
                                            class="btn btn-sm btn-outline-danger"
                                            title="Reject"
                                            @click="editCompanyStatus(company.id, 'reject')"
                                        >
                                            Reject
                                        </button>
                                    </template>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div class="card-footer text-muted text-center">
                Showing {{ filteredAndSortedCompanies().length }} of {{ companies.length }} companies
            </div>
        </div>

        <!-- Empty State -->
        <div v-else class="card text-center py-5">
            <div class="card-body">
                <h5 class="card-title">No Companies Found</h5>
                <p class="card-text text-muted">
                    No companies match your search criteria.
                </p>
                <button 
                    @click="searchQuery = ''; filterStatus = 'all'"
                    class="btn btn-outline-primary"
                >
                    Clear Filters
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
