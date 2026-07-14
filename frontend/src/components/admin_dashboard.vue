<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();

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

const searchQuery = ref("");
const searchType = ref("students");

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: "/admin/search",
      query: { q: searchQuery.value.trim(), type: searchType.value },
    });
  }
};
</script>

<template>
  <div class="container">
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-primary fs-3 d-flex align-items-center gap-2">
          <i class="bi bi-mortarboard-fill"></i> Nexus <span class="fs-6 text-muted ms-2 fw-normal">| Admin</span>
        </span>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin"><b>Dashboard</b></router-link>
            </li>
            <li class="nav-item dropdown">
              <a
                class="nav-link dropdown-toggle"
                href="#"
                role="button"
                data-bs-toggle="dropdown"
                aria-expanded="false"
              >
                Manage
              </a>
              <ul class="dropdown-menu">
                <li>
                  <router-link class="dropdown-item" to="/admin/students"
                    >Student List</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/companies"
                    >Company List</router-link
                  >
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/placement-drives"
                    >Placement Drives</router-link
                  >
                </li>
                <li>
                  <hr class="dropdown-divider" />
                </li>
                <li>
                  <router-link class="dropdown-item" to="/admin/applications"
                    >Applications</router-link
                  >
                </li>
              </ul>
            </li>
          </ul>
          <form class="d-flex" role="search" @submit.prevent="handleSearch">
            <select v-model="searchType" class="form-select me-2" style="width: auto;">
              <option value="students">Students</option>
              <option value="companies">Companies</option>
              <option value="placement-drives">Placement Drives</option>
            </select>
            <input
              v-model="searchQuery"
              class="form-control me-3"
              type="search"
              placeholder="Search"
              aria-label="Search"
            />
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
          <button class="btn btn-outline-danger ms-3" @click="handleLogout">
            Logout
          </button>
        </div>
      </div>
    </nav>
    <div class="mt-5">
      <router-view :key="$route.path" />
    </div>
  </div>
</template>

<style scoped></style>
