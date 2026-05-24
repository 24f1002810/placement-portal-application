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
  dob: ""
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
      dob: studentForm.value.dob
    });

    successMessage.value = "Student registration successful! Redirecting to login...";
    setTimeout(() => {
      router.push("/login");
    }, 1500);
  } catch (error) {
    errorMessage.value =
      error.response?.data?.message || "Registration failed. Please try again.";
    console.error("Student registration failed:", error);
  } finally {
    isLoading.value = false;
  }
};

const handleCompanyRegister = async () => {
  // Validation
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
  <div class="register-container">
    <div class="register-card">
      <h2>Create Your Account</h2>
      <p>Join our placement portal</p>

      <!-- Type Selector -->
      <div class="type-selector">
        <button
          :class="['type-btn', { active: registrationType === 'student' }]"
          @click="registrationType = 'student'"
          :disabled="isLoading"
        >
          <span class="icon">👨‍🎓</span> Student Registration
        </button>
        <button
          :class="['type-btn', { active: registrationType === 'company' }]"
          @click="registrationType = 'company'"
          :disabled="isLoading"
        >
          <span class="icon">🏢</span> Company Registration
        </button>
      </div>

      <!-- Messages -->
      <div v-if="errorMessage" class="error-alert">
        {{ errorMessage }}
      </div>
      <div v-if="successMessage" class="success-alert">
        {{ successMessage }}
      </div>

      <!-- Student Registration Form -->
      <form v-if="registrationType === 'student'" @submit.prevent="handleStudentRegister">
        <div class="form-group">
          <label for="student-name">Full Name</label>
          <input
            type="text"
            id="student-name"
            v-model="studentForm.name"
            required
            placeholder="Enter your full name"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="student-email">Email</label>
          <input
            type="email"
            id="student-email"
            v-model="studentForm.email"
            required
            placeholder="your.email@example.com"
            :disabled="isLoading"
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="student-roll">Roll Number</label>
            <input
              type="text"
              id="student-roll"
              v-model="studentForm.rollNo"
              required
              placeholder="e.g., 2021001"
              :disabled="isLoading"
            />
          </div>
          <div class="form-group">
            <label for="student-dob">Date of Birth</label>
            <input
              type="date"
              id="student-dob"
              v-model="studentForm.dob"
              required
              :disabled="isLoading"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="student-phone">Phone Number</label>
          <input
            type="tel"
            id="student-phone"
            v-model="studentForm.phone"
            placeholder="+91 9876543210"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="student-password">Password</label>
          <input
            type="password"
            id="student-password"
            v-model="studentForm.password"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="student-confirm-password">Confirm Password</label>
          <input
            type="password"
            id="student-confirm-password"
            v-model="studentForm.confirmPassword"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? "Registering..." : "Register as Student" }}
        </button>
      </form>

      <!-- Company Registration Form -->
      <form v-else @submit.prevent="handleCompanyRegister">
        <div class="form-group">
          <label for="company-name">Company Name</label>
          <input
            type="text"
            id="company-name"
            v-model="companyForm.companyName"
            required
            placeholder="Enter company name"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="company-email">Company Email</label>
          <input
            type="email"
            id="company-email"
            v-model="companyForm.email"
            required
            placeholder="hr@company.com"
            :disabled="isLoading"
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="company-industry">Industry</label>
            <select
              id="company-industry"
              v-model="companyForm.industry"
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

          <div class="form-group">
            <label for="company-hr">HR Contact</label>
            <input
              type="text"
              id="company-hr"
              v-model="companyForm.hrContact"
              required
              placeholder="HR Manager name"
              :disabled="isLoading"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="company-website">Website</label>
          <input
            type="url"
            id="company-website"
            v-model="companyForm.website"
            placeholder="https://www.company.com"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="company-location">Location</label>
          <textarea
            id="company-location"
            v-model="companyForm.location"
            required
            placeholder="Company location/address"
            rows="2"
            :disabled="isLoading"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="company-description">Company Description</label>
          <textarea
            id="company-description"
            v-model="companyForm.description"
            required
            placeholder="Brief description of your company"
            rows="3"
            :disabled="isLoading"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="company-password">Password</label>
          <input
            type="password"
            id="company-password"
            v-model="companyForm.password"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="company-confirm-password">Confirm Password</label>
          <input
            type="password"
            id="company-confirm-password"
            v-model="companyForm.confirmPassword"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? "Registering..." : "Register as Company" }}
        </button>
      </form>

      <p class="login-link">
        Already have an account? <router-link to="/login">Sign In</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f3f4f6;
  padding: 1rem;
}

.register-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  width: 100%;
  max-width: 600px;
}

h2 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #1f2937;
  font-size: 1.875rem;
}

p {
  color: #6b7280;
  margin-bottom: 1.5rem;
}

/* Type Selector */
.type-selector {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
}

.type-btn {
  flex: 1;
  padding: 1rem;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 500;
  color: #6b7280;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.type-btn:hover {
  border-color: #3b82f6;
  color: #3b82f6;
  background: #eff6ff;
}

.type-btn.active {
  border-color: #3b82f6;
  background: #eff6ff;
  color: #3b82f6;
  font-weight: 600;
}

.type-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.icon {
  font-size: 1.5rem;
}

/* Form Styles */
form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  margin-bottom: 0.5rem;
  color: #374151;
  font-weight: 500;
  font-size: 0.875rem;
}

input,
select,
textarea {
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

input:focus,
select:focus,
textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

input:disabled,
select:disabled,
textarea:disabled {
  background-color: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

textarea {
  resize: vertical;
}

/* Alert Styles */
.error-alert {
  padding: 0.75rem 1rem;
  background-color: #fee2e2;
  color: #dc2626;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  border-left: 4px solid #dc2626;
}

.success-alert {
  padding: 0.75rem 1rem;
  background-color: #dcfce7;
  color: #16a34a;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  border-left: 4px solid #16a34a;
}

/* Submit Button */
.submit-btn {
  padding: 0.75rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
  margin-top: 0.5rem;
}

.submit-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.submit-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

/* Login Link */
.login-link {
  text-align: center;
  margin-top: 1.5rem;
  margin-bottom: 0;
  color: #6b7280;
  font-size: 0.875rem;
}

.login-link a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s;
}

.login-link a:hover {
  color: #2563eb;
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 640px) {
  .register-card {
    padding: 1.5rem;
  }

  .type-selector {
    flex-direction: column;
  }

  .form-row {
    grid-template-columns: 1fr;
  }

  h2 {
    font-size: 1.5rem;
  }
}
</style>
