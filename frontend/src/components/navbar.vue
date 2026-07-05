<script setup>
import { computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

const user = computed(() => store.getters["user/getUser"]);
const role = computed(() => store.getters["user/getUserRole"]); // Convert user to string for display
const isLoading = computed(() => store.getters["user/isLoading"]);

// If not authenticated, redirect to login
if (!store.getters["user/isAuthenticated"]) {
  router.push({ name: "Login" });
}

const handleLogout = async () => {
  try {
    await store.dispatch("user/logout");
    router.push({ name: "Login" });
  } catch (error) {
    console.error("Logout error:", error);
    router.push({ name: "Login" });
  }
};
</script>
<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <span class="navbar-brand">{{ role }} Dashboard</span>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <ul class="nav nav-underline nav-justify">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/students"
                >Student List</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/companies"
                >Company List</router-link
              >
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin/placement-drives"
                >Placement Drives</router-link
              >
            </li>
          </ul>
        </ul>
        <form class="d-flex" role="search">
          <input
            class="form-control me-3"
            type="search"
            placeholder="Search"
            aria-label="Search"
          />
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form>
        <button class="btn btn-outline-danger ms-3" @click="handleLogout">Logout</button>
      </div>
    </div>
  </nav>

  <div class="mt-3">
    <router-view />
  </div>
</template>

<style scoped>
.dashboard-container {
  padding: 2rem;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f3f4f6;
  padding: 1rem;
  border-radius: 4px;
  margin-bottom: 2rem;
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: 600;
  color: #1f2937;
}

.btn-logout {
  background-color: #ef4444;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.btn-logout:hover {
  background-color: #dc2626;
}

h1 {
  color: #1f2937;
  margin-bottom: 2rem;
}

.message-box {
  background-color: #dbeafe;
  color: #1e40af;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
  font-size: 1.1rem;
}

.loading {
  color: #6b7280;
  font-size: 1rem;
  margin-top: 1rem;
}

.error-alert {
  background-color: #fee2e2;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 4px;
  margin-top: 1rem;
}

.profile-info {
  margin-top: 1.5rem;
  text-align: left;
  display: inline-block;
  background-color: #f3f4f6;
  padding: 1rem;
  border-radius: 4px;
}
</style>
