<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";

const route = useRoute();
const router = useRouter();
const studentId = route.params.id;

const loading = ref(true);
const saving = ref(false);
const error = ref("");
const success = ref("");
const form = ref({
  name: "",
  email: "",
  phone_number: "",
  dob: "",
  education: "",
  skills: "",
  working_experience: 0,
  cgpa: 0,
});

onMounted(async () => {
  try {
    const response = await api.get(`/api/student/${studentId}`);
    const student = response.data.student || {};

    form.value = {
      name: student.name || "",
      email: student.email || "",
      phone_number: student.phone_number || "",
      dob: student.dob ? student.dob.split("T")[0] : "",
      education: student.education || "",
      skills: Array.isArray(student.skills)
        ? student.skills.join(", ")
        : student.skills || "",
      working_experience: student.working_experience ?? 0,
      cgpa: student.cgpa ?? 0,
    };
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load student details";
    console.error("Load student error:", err);
  } finally {
    loading.value = false;
  }
});

async function submitForm() {
  saving.value = true;
  error.value = "";
  success.value = "";

  try {
    const payload = {
      name: form.value.name,
      phone_number: form.value.phone_number,
      dob: form.value.dob,
      education: form.value.education,
      skills: form.value.skills,
      working_experience: Number(form.value.working_experience),
      cgpa: Number(form.value.cgpa),
    };

    const response = await api.post(`/api/student/${studentId}`, payload);
    success.value = response.data.message || "Student details updated successfully.";

    setTimeout(() => {
      router.push({ name: "StudentProfile", params: { id: studentId } });
    }, 600);
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to update student details";
    console.error("Update student error:", err);
  } finally {
    saving.value = false;
  }
}

</script>

<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow-sm">
          <div
            class="card-header bg-primary text-white d-flex justify-content-between align-items-center"
          >
            <div>
              <h4 class="mb-0">Edit Student Details</h4>
              <small class="text-light">Update academic and personal information</small>
            </div>
            <button class="btn btn-light btn-sm" @click="router.back()">Back</button>
          </div>

          <div class="card-body">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <div v-else>
              <div v-if="error" class="alert alert-danger">{{ error }}</div>
              <div v-if="success" class="alert alert-success">{{ success }}</div>

              <form @submit.prevent="submitForm">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label">Full Name</label>
                    <input
                      v-model="form.name"
                      type="text"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Email</label>
                    <input
                      v-model="form.email"
                      type="email"
                      class="form-control"
                      disabled
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Phone Number</label>
                    <input
                      v-model="form.phone_number"
                      type="text"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Date of Birth</label>
                    <input v-model="form.dob" type="date" class="form-control" required />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Education</label>
                    <input
                      v-model="form.education"
                      type="text"
                      class="form-control"
                      placeholder="e.g. B.Tech Computer Science"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">CGPA</label>
                    <input
                      v-model="form.cgpa"
                      type="number"
                      step="0.01"
                      min="0"
                      class="form-control"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Skills</label>
                    <input
                      v-model="form.skills"
                      type="text"
                      class="form-control"
                      placeholder="Python, Java, SQL"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Working Experience (years)</label>
                    <input
                      v-model="form.working_experience"
                      type="number"
                      min="0"
                      class="form-control"
                    />
                  </div>
                </div>

                <div class="d-flex justify-content-end gap-2 mt-4">
                  <button type="button" class="btn btn-outline-secondary" @click="router.back()">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="saving">
                    <span
                      v-if="saving"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                    ></span>
                    {{ saving ? "Saving..." : "Save Changes" }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
