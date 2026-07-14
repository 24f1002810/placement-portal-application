<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/api";

const registrationType = ref("student"); // 'student' or 'company'
const isLoading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");
const router = useRouter();

// Student form fields
const studentForm = ref({
  name: "",
  email: "",
  password: "",
  confirmPassword: "",
  rollNo: "",
  phone: "",
  dob: "",
});

// Company form fields
const companyForm = ref({
  companyName: "",
  email: "",
  password: "",
  confirmPassword: "",
  industry: "",
  website: "",
  hrContact: "",
  location: "",
  description: "",
});

const handleStudentRegister = async () => {
  // Validation
  if (studentForm.value.password !== studentForm.value.confirmPassword) {
    errorMessage.value = "Passwords do not match";
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    const response = await api.post("/register", {
      name: studentForm.value.name,
      email: studentForm.value.email,
      password: studentForm.value.password,
      role: "student",
      rollNo: studentForm.value.rollNo,
      cgpa: studentForm.value.cgpa,
      phone: studentForm.value.phone,
      dob: studentForm.value.dob,
    });

    successMessage.value = "Student registration successful! Redirecting to login...";
    setTimeout(() => {
      router.push("/login");
    }, 1500);
  } catch (error) {
    errorMessage.value = "Registration Failed";
    console.error("Student registration failed:", error.response.data.message);
  } finally {
    isLoading.value = false;
  }
};

const handleCompanyRegister = async () => {
  if (companyForm.value.password !== companyForm.value.confirmPassword) {
    errorMessage.value = "Passwords do not match";
    return;
  }

  isLoading.value = true;
  errorMessage.value = "";
  successMessage.value = "";

  try {
    const response = await api.post("/register", {
      companyName: companyForm.value.companyName,
      email: companyForm.value.email,
      password: companyForm.value.password,
      role: "company",
      industry: companyForm.value.industry,
      website: companyForm.value.website,
      hrContact: companyForm.value.hrContact,
      location: companyForm.value.location,
      description: companyForm.value.description,
    });

    successMessage.value = "Company registration successful! Redirecting to login...";
    setTimeout(() => {
      router.push("/login");
    }, 1500);
  } catch (error) {
    errorMessage.value =
      error.response?.data?.message || "Registration failed. Please try again.";
    console.error("Company registration failed:", error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="d-flex justify-content-center align-items-center min-vh-100 bg-light py-5 px-3">
    <div class="card shadow border-0 p-4 p-md-5 w-100" style="max-width: 600px; border-radius: 12px;">
      <div class="text-center mb-4">
        <h2 class="fw-bold text-dark mb-2">Create Your Account</h2>
        <p class="text-muted">Join our placement portal</p>
      </div>

      <div class="d-flex gap-3 mb-4 flex-column flex-sm-row">
        <button
          :class="['btn flex-fill py-3 border', registrationType === 'student' ? 'btn-primary border-primary shadow-sm' : 'btn-light text-muted']"
          @click="registrationType = 'student'"
          :disabled="isLoading"
        >
          <span class="fs-4 d-block mb-1">👨‍🎓</span> 
          <span class="fw-medium">Student Registration</span>
        </button>
        <button
          :class="['btn flex-fill py-3 border', registrationType === 'company' ? 'btn-primary border-primary shadow-sm' : 'btn-light text-muted']"
          @click="registrationType = 'company'"
          :disabled="isLoading"
        >
          <span class="fs-4 d-block mb-1">🏢</span> 
          <span class="fw-medium">Company Registration</span>
        </button>
      </div>

      <div v-if="errorMessage" class="alert alert-danger shadow-sm border-0 border-start border-danger border-4">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="alert alert-success shadow-sm border-0 border-start border-success border-4">
        {{ successMessage }}
      </div>

      <form v-if="registrationType === 'student'" @submit.prevent="handleStudentRegister" class="d-flex flex-column gap-3">
        <div class="form-group">
          <label for="student-name" class="form-label fw-medium text-secondary small mb-1">Full Name</label>
          <input
            type="text"
            id="student-name"
            v-model="studentForm.name"
            class="form-control"
            required
            placeholder="Enter your full name"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="student-email" class="form-label fw-medium text-secondary small mb-1">Email</label>
          <input
            type="email"
            id="student-email"
            v-model="studentForm.email"
            class="form-control"
            required
            placeholder="your.email@example.com"
            :disabled="isLoading"
          />
        </div>

        <div class="row g-3">
          <div class="col-sm-6">
            <label for="student-roll" class="form-label fw-medium text-secondary small mb-1">Roll Number</label>
            <input
              type="text"
              id="student-roll"
              v-model="studentForm.rollNo"
              class="form-control"
              required
              placeholder="e.g., 2021001"
              :disabled="isLoading"
            />
          </div>
          <div class="col-sm-6">
            <label for="student-dob" class="form-label fw-medium text-secondary small mb-1">Date of Birth</label>
            <input
              type="date"
              id="student-dob"
              v-model="studentForm.dob"
              class="form-control"
              required
              :disabled="isLoading"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="student-phone" class="form-label fw-medium text-secondary small mb-1">Phone Number</label>
          <input
            type="tel"
            id="student-phone"
            v-model="studentForm.phone"
            class="form-control"
            placeholder="+91 9876543210"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="student-password" class="form-label fw-medium text-secondary small mb-1">Password</label>
          <input
            type="password"
            id="student-password"
            v-model="studentForm.password"
            class="form-control"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="student-confirm-password" class="form-label fw-medium text-secondary small mb-1">Confirm Password</label>
          <input
            type="password"
            id="student-confirm-password"
            v-model="studentForm.confirmPassword"
            class="form-control"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <button type="submit" class="btn btn-primary w-100 py-2 mt-3 fw-semibold shadow-sm" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          {{ isLoading ? "Registering..." : "Register as Student" }}
        </button>
      </form>

      <form v-else @submit.prevent="handleCompanyRegister" class="d-flex flex-column gap-3">
        <div class="form-group">
          <label for="company-name" class="form-label fw-medium text-secondary small mb-1">Company Name</label>
          <input
            type="text"
            id="company-name"
            v-model="companyForm.companyName"
            class="form-control"
            required
            placeholder="Enter company name"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="company-email" class="form-label fw-medium text-secondary small mb-1">Company Email</label>
          <input
            type="email"
            id="company-email"
            v-model="companyForm.email"
            class="form-control"
            required
            placeholder="company@domain.com"
            :disabled="isLoading"
          />
        </div>

        <div class="row g-3">
          <div class="col-sm-6">
            <label for="company-industry" class="form-label fw-medium text-secondary small mb-1">Industry</label>
            <select
              id="company-industry"
              v-model="companyForm.industry"
              class="form-select"
              required
              :disabled="isLoading"
            >
              <option value="">Select Industry</option>
              <option value="it">Information Technology</option>
              <option value="finance">Finance</option>
              <option value="manufacturing">Manufacturing</option>
              <option value="retail">Retail</option>
              <option value="healthcare">Healthcare</option>
              <option value="education">Education</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div class="col-sm-6">
            <label for="company-hr" class="form-label fw-medium text-secondary small mb-1">HR Contact</label>
            <input
              type="text"
              id="company-hr"
              v-model="companyForm.hrContact"
              class="form-control"
              required
              placeholder="HR Manager name"
              :disabled="isLoading"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="company-website" class="form-label fw-medium text-secondary small mb-1">Website</label>
          <input
            type="url"
            id="company-website"
            v-model="companyForm.website"
            class="form-control"
            placeholder="https://www.company.com"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="company-location" class="form-label fw-medium text-secondary small mb-1">Location</label>
          <textarea
            id="company-location"
            v-model="companyForm.location"
            class="form-control"
            required
            placeholder="Company location/address"
            rows="2"
            :disabled="isLoading"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="company-description" class="form-label fw-medium text-secondary small mb-1">Company Description</label>
          <textarea
            id="company-description"
            v-model="companyForm.description"
            class="form-control"
            required
            placeholder="Brief description of your company"
            rows="3"
            :disabled="isLoading"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="company-password" class="form-label fw-medium text-secondary small mb-1">Password</label>
          <input
            type="password"
            id="company-password"
            v-model="companyForm.password"
            class="form-control"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="company-confirm-password" class="form-label fw-medium text-secondary small mb-1">Confirm Password</label>
          <input
            type="password"
            id="company-confirm-password"
            v-model="companyForm.confirmPassword"
            class="form-control"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <button type="submit" class="btn btn-primary w-100 py-2 mt-3 fw-semibold shadow-sm" :disabled="isLoading">
          <span v-if="isLoading" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
          {{ isLoading ? "Registering..." : "Register as Company" }}
        </button>
      </form>

      <p class="text-center text-muted mt-4 mb-0 small">
        Already have an account? <router-link to="/login" class="text-primary text-decoration-none fw-semibold">Sign In</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Styles handled via Bootstrap utilities */
</style>
