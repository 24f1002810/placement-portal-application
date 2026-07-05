<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";

const route = useRoute();
const router = useRouter();
const loading = ref(true);
const error = ref("");
const student = ref(null);

onMounted(async () => {
  try {
    const studentId = route.params.id;
    const response = await api.get(`api/student/${studentId}`);
    student.value = response.data.student;
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load student details";
    console.error("Student details error:", err);
  } finally {
    loading.value = false;
  }
});

const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};

const calculateAge = (dateString) => {
  if (!dateString) return "N/A";
  const today = new Date();
  const birthDate = new Date(dateString);
  let age = today.getFullYear() - birthDate.getFullYear();
  const monthDiff = today.getMonth() - birthDate.getMonth();
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
};

const getSkillsArray = (skillsData) => {
  if (!skillsData) return [];
  // Skills is already an array from backend
  if (Array.isArray(skillsData)) {
    return skillsData;
  }
  // Fallback: if it's a string, split it
  return skillsData
    .split(",")
    .map((skill) => skill.trim())
    .filter((skill) => skill);
};

function editStudent() {
  if (student.value?.id) {
    router.push({ name: "EditStudent", params: { id: student.value.id } });
  }
}

function deleteStudent() {
  if (confirm("Are you sure you want to delete this student?")) {
    api
      .delete(`api/student/${student.value.id}`)
      .then((response) => {
        alert(response.data.message || "Student deleted successfully.");
        router.push({ name: "StudentList" });
      })
      .catch((err) => {
        console.error("Error deleting student:", err);
        alert("Failed to delete the student.");
      });
  }
}

function updateBlockStatus(id, is_blocked) {
  if (id) {
    api
      .post(`api/student/${id}`, { 'block': is_blocked })
      .then((response) => {
        alert(response.data.message || "Student blocked status updated successfully.");
        student.value.blocked = is_blocked;
      })
      .catch((err) => {
        console.error("Error updating student block status:", err);
        alert("Failed to update student block status.");
      });
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

    <div v-else-if="student" class="row">
      <div v-if="student.blocked" class="col-12 mb-3">
        <div class="alert alert-warning d-flex align-items-center mb-0" role="alert">
          <strong class="me-2">Account Disabled</strong>
          <span>This student's account is currently disabled.</span>
        </div>
      </div>

      <div class="col-lg-8">
        <!-- Student Header Card -->
        <div class="card mb-4">
          <div class="card-header bg-primary text-white">
            <div class="row align-items-center">
              <div class="col">
                <h2 class="mb-0">{{ student.name }}</h2>
                <p class="mb-0 mt-2 text-light">Student ID: {{ student.id }}</p>
              </div>
              <div class="col-auto">
                <div class="text-center">
                  <div class="display-6" style="color: #ffd700">⭐</div>
                  <small class="text-light">CGPA: {{ student.cgpa }}</small>
                </div>
              </div>
            </div>
          </div>
          <div class="card-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <h6 class="text-muted">Email</h6>
                <p class="fs-6">
                  <a :href="`mailto:${student.email}`">{{ student.email }}</a>
                </p>
              </div>
              <div class="col-md-6">
                <h6 class="text-muted">Phone</h6>
                <p class="fs-6">
                  <a :href="`tel:${student.phone_number}`">{{ student.phone_number }}</a>
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Personal Information Card -->
        <div class="card mb-4">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Personal Information</h5>
          </div>
          <div class="card-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <h6 class="text-muted">Date of Birth</h6>
                <p class="fs-6">{{ formatDate(student.dob) }}</p>
              </div>
              <div class="col-md-6">
                <h6 class="text-muted">Age</h6>
                <p class="fs-6">{{ calculateAge(student.dob) }} years</p>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <h6 class="text-muted">Phone Number</h6>
                <p class="fs-6">{{ student.phone_number }}</p>
              </div>
              <div class="col-md-6">
                <h6 class="text-muted">Email Address</h6>
                <p class="fs-6">{{ student.email }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Academic Information Card -->
        <div class="card mb-4">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Academic Information</h5>
          </div>
          <div class="card-body">
            <div class="row mb-3">
              <div class="col-md-6">
                <h6 class="text-muted">CGPA</h6>
                <p class="fs-6">
                  <strong class="text-success">{{ student.cgpa }}</strong>
                </p>
              </div>
              <div class="col-md-6">
                <h6 class="text-muted">Education</h6>
                <p class="fs-6">{{ student.education || "N/A" }}</p>
              </div>
            </div>
            <div class="row">
              <div class="col-12">
                <h6 class="text-muted">Skills</h6>
                <div v-if="getSkillsArray(student.skills).length > 0" class="mt-2">
                  <span
                    v-for="(skill, index) in getSkillsArray(student.skills)"
                    :key="index"
                    class="badge bg-info text-dark me-2 mb-2"
                  >
                    {{ skill }}
                  </span>
                </div>
                <p v-else class="text-muted">No skills listed</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Experience Card -->
        <div class="card mb-4">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Professional Information</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-6">
                <h6 class="text-muted">Working Experience</h6>
                <p class="fs-6">
                  <strong>{{ student.working_experience || 0 }}</strong> years
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <div class="col-lg-4">
        <!-- Quick Stats Card -->
        <div class="card sticky-top mb-3">
          <div class="card-header bg-info text-white">
            <h5 class="mb-0">Quick Actions</h5>
          </div>
          <div class="card-body d-grid gap-2">
            <button class="btn btn-primary" @click="editStudent">Edit Profile</button>
            <button class="btn btn-info">View Applications</button>
            <button class="btn btn-warning">Download Resume</button>
            <button class="btn btn-danger" @click="deleteStudent">Delete Account</button>
            <button v-if="student.blocked" @click="updateBlockStatus(student.id, false)" class="btn btn-success">Unblock</button>
            <button v-else @click="updateBlockStatus(student.id, true)" class="btn btn-warning">Block</button>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="alert alert-info text-center">No student data available</div>
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
  font-size: 0.85rem;
  padding: 0.5rem 0.75rem;
}

.btn {
  font-weight: 500;
  padding: 0.6rem 1rem;
}

.progress {
  height: 1.5rem;
}

.progress-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 0.85rem;
}

.display-6 {
  line-height: 1;
}

.d-grid.gap-2 > * + * {
  margin-top: 0.5rem;
}
</style>
