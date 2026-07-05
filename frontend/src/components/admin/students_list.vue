<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";
import { useRouter } from "vue-router";

const router = useRouter();
const loading = ref(true);
const error = ref("");
const students = ref([]);
const searchQuery = ref("");
const sortBy = ref("name");
const sortOrder = ref("asc");

onMounted(async () => {
  await fetchStudents();
});

const fetchStudents = async () => {
  loading.value = true;
  error.value = "";
  try {
    const response = await api.get("api/admin/students");
    students.value = response.data.students;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load students";
    console.error("Students list error:", err);
  } finally {
    loading.value = false;
  }
};

const filteredAndSortedStudents = () => {
  let filtered = students.value.filter((student) => {
    const query = searchQuery.value.toLowerCase();
    return (
      student.name.toLowerCase().includes(query) ||
      student.email.toLowerCase().includes(query) ||
      student.phone_number.includes(query)
    );
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

const viewStudentDetails = (studentId) => {
  router.push(`/student/${studentId}`);
};

const getCGPABadgeClass = (cgpa) => {
  if (cgpa >= 7.0) return "bg-success";
  if (cgpa < 7.0 && cgpa >= 5.0) return "bg-info";
  if (cgpa < 5.0) return "bg-warning";
  return "bg-danger";
};

const isStudentActive = (student) => {
  return student?.active ?? student?.user_account?.active ?? true;
};

// const updateStudentAccountStatus = (studentId, isActive) => {
//   students.value = students.value.map((student) => {
//     if (student.id !== studentId) return student;

//     return {
//       ...student,
//       active: isActive,
//       user_account: {
//         ...(student.user_account || {}),
//         active: isActive,
//       },
//     };
//   });
// };

function editStudent(id) {
  if (id) {
    router.push({ name: "EditStudent", params: { id: id } });
  }
}

function deleteStudent(id) {
  if (confirm("Do you want to delete this student?")) {
    api
      .delete(`api/student/${id}`)
      .then((response) => {
        alert(response.data.message || "Student deleted successfully.");
        router.push({ name: "StudentList" });
      })
      .catch((err) => {
        console.error("Error in deleting student:", err);
        alert("Failed to delete the student");
      });
  }
}

function updateBlockStatus(s_id ,is_blocked) {
  if (s_id) {
    api
      .post(`api/student/${s_id}`, { 'block': is_blocked })
      .then((response) => {
        alert(response.data.message || "Student blocked status updated successfully.");
        const student = students.value.find(s => s.id === s_id);
        if (student) {
          student.active = !is_blocked;
        }
      })
      .catch((err) => {
        console.error("Error updating student block status:", err);
        alert("Failed to update student block status.");
      });
  }
}
</script>

<template>
  <div class="container-fluid mt-5 mb-5">
    <!-- Header Section -->
    <div class="row mb-4">
      <div class="col">
        <h1 class="display-5">Registered Students</h1>
        <p class="text-muted">Manage and view all student profiles</p>
      </div>
      <div class="col-auto">
        <div class="badge bg-primary text-white p-3" v-if="!loading">
          <h6 class="mb-0">Total Students: {{ students.length }}</h6>
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
          <div class="col-md-8">
            <input
              v-model="searchQuery"
              type="text"
              class="form-control form-control-lg"
              placeholder="Search by name, email, or phone..."
            />
          </div>
          <div class="col-md-4">
            <button
              @click="fetchStudents"
              class="btn btn-primary w-100"
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
      <p class="mt-3 text-muted">Loading students...</p>
    </div>

    <!-- Students Table -->
    <div v-else-if="filteredAndSortedStudents().length > 0" class="card">
      <div class="table-responsive">
        <table class="table table-hover mb-0">
          <thead class="table-light">
            <tr>
              <th class="cursor-pointer" @click="toggleSort('id')">
                ID {{ getSortIcon("id") }}
              </th>
              <th class="cursor-pointer" @click="toggleSort('name')">
                Name {{ getSortIcon("name") }}
              </th>
              <th class="cursor-pointer" @click="toggleSort('email')">
                Email {{ getSortIcon("email") }}
              </th>
              <th>Phone</th>
              <th class="cursor-pointer" @click="toggleSort('cgpa')">
                CGPA {{ getSortIcon("cgpa") }}
              </th>
              <th class="text-center">Skills</th>
              <th class="text-center">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in filteredAndSortedStudents()" :key="student.id">
              <td class="align-middle">
                <span class="badge bg-secondary">{{ student.id }}</span>
              </td>
              <td class="align-middle fw-500">{{ student.name }}</td>
              <td class="align-middle">
                <a :href="`mailto:${student.email}`" class="text-decoration-none">
                  {{ student.email }}
                </a>
              </td>
              <td class="align-middle">
                <a :href="`tel:${student.phone_number}`" class="text-decoration-none">
                  {{ student.phone_number }}
                </a>
              </td>
              <td class="align-middle">
                <span :class="['badge', getCGPABadgeClass(student.cgpa)]">
                  {{ student.cgpa }}
                </span>
              </td>
              <td class="align-middle text-center">
                <span
                  v-if="student.skills && student.skills.length > 0"
                  class="badge bg-info text-dark"
                >
                  {{ student.skills.length }}
                </span>
                <span v-else class="text-muted">-</span>
              </td>
              <td class="align-middle text-center">
                <button
                  @click="viewStudentDetails(student.id)"
                  class="btn btn-sm btn-info me-2"
                  title="View Details"
                >
                  View
                </button>
                <button
                  class="btn btn-sm btn-warning me-2"
                  title="Edit"
                  @click="editStudent(student.id)"
                >
                  Edit
                </button>
                <button
                  class="btn btn-sm btn-danger me-2"
                  title="Delete"
                  @click="deleteStudent(student.id)"
                >
                  Delete
                </button>
                <button
                  v-if="isStudentActive(student)"
                  class="btn btn-sm btn-secondary me-2"
                  title="Block"
                  @click="updateBlockStatus(student.id, true)"
                >
                  Block
                </button>
                <button
                  v-else
                  class="btn btn-sm btn-success text-white me-2"
                  title="Unblock"
                  @click="updateBlockStatus(student.id, false)"
                >
                  Unblock
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="card-footer bg-light text-muted text-center py-3">
        Showing {{ filteredAndSortedStudents().length }} of {{ students.length }} students
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="alert alert-info text-center py-5">
      <h5>No Students Found</h5>
      <p class="mb-0">
        {{
          searchQuery
            ? "No students match your search criteria"
            : "No registered students yet"
        }}
      </p>
    </div>
  </div>
</template>

<style scoped>
.table {
  font-size: 0.95rem;
}

.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}

thead th {
  font-weight: 600;
  text-transform: uppercase;
  font-size: 0.85rem;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #dee2e6;
}

.cursor-pointer {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
}

.cursor-pointer:hover {
  background-color: #e9ecef;
}

.badge {
  font-size: 0.85rem;
  padding: 0.5rem 0.75rem;
}

.btn-sm {
  font-size: 0.85rem;
  padding: 0.4rem 0.75rem;
}

.fw-500 {
  font-weight: 500;
}

.display-5 {
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.card {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  border: none;
  transition: box-shadow 0.3s ease;
}

.card:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.table-responsive {
  border-radius: 0.25rem;
}

@media (max-width: 768px) {
  .table {
    font-size: 0.85rem;
  }

  .btn-sm {
    padding: 0.3rem 0.5rem;
    font-size: 0.75rem;
  }

  thead th {
    font-size: 0.75rem;
  }
}
</style>
