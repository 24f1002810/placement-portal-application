<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";
import api from "@/services/api";

const email = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);
const router = useRouter();
const store = useStore();

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const user = await store.dispatch("user/login", {
      email: email.value,
      password: password.value,
    });

    console.log("User logged in:", user);
    console.log("Store isAuthenticated:", store.getters["user/isAuthenticated"]);
    console.log("Store isAdmin:", store.getters["user/isAdmin"]);
    console.log("Store user:", store.getters["user/getUser"]);

    if (user.role === "admin") {
      console.log("Redirecting to AdminHome");
      router.push({ name: "AdminHome" });
    } 
    else if (user.role === "company") {
      if (user.approval_status === "approved") {
        console.log("Redirecting to company Dashboard");
        router.push(`/company/${user.companyId}`);
      }
      else {
        errorMessage.value = "Your company account is not approved yet.";
      }
    }
    else if(user.role === "student"){
      console.log("Redirecting to StudentDashboard");
      router.push(`/student/${user.studentId}`);
    }
    else{
      errorMessage.value = "You are not authorized to login.";
    }
  } catch (error) {
    const responseData = error.response?.data?.response;
    
    let specificError = "";
    if (responseData?.errors && responseData.errors.length > 0) {
      specificError = responseData.errors[0];
    } 
    else if (responseData?.field_errors) {
      const fields = Object.values(responseData.field_errors);
      if (fields.length > 0 && fields[0].length > 0) {
        specificError = fields[0][0];
      }
    }
    
    errorMessage.value =
      specificError ||
      error.response?.data?.response?.message ||
      error.response?.data?.message ||
      "Invalid email or password.";
      
    console.error("Login failed:", error);
  } finally {
    isLoading.value = false;
  }
};

const register = () => {
  router.push({ name: "Register" });
};
</script>
<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Welcome Back</h2>
      <p>Please sign in to your account</p>

      <div v-if="errorMessage" class="error-alert">
        {{ errorMessage }}
      </div>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            required
            placeholder="admin@test.com"
            :disabled="isLoading"
          />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input
            type="password"
            id="password"
            v-model="password"
            required
            placeholder="••••••••"
            :disabled="isLoading"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="isLoading">
          {{ isLoading ? "Signing In..." : "Sign In" }}
        </button>
      </form>
      <p class="m-3">New User? <a href="#" @click="register">Register Here</a></p>
    </div>
  </div>
</template>
<style>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f3f4f6;
}

.login-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  width: 100%;
  max-width: 400px;
}

h2 {
  margin-top: 0;
  margin-bottom: 0.5rem;
  color: #1f2937;
}

p {
  color: #6b7280;
  margin-bottom: 1.5rem;
  font-size: 0.875rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background-color: #2563eb;
}

.submit-btn:disabled {
  background-color: #9ca3af;
  cursor: not-allowed;
}

.error-alert {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
  font-size: 0.875rem;
  text-align: center;
}
</style>
