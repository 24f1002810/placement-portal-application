<script setup>
import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const store = useStore();
const router = useRouter();
const studentId = store.getters['user/getStudentId']

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
const searchType = ref("applications");

const handleSearch = () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: `/student/${studentId}/search`,
      query: { q: searchQuery.value.trim(), type: searchType.value },
    });
  }
};
</script>
<template>
  <div>
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <span class="navbar-brand fw-bold text-primary fs-3 d-flex align-items-center gap-2">
          <i class="bi bi-mortarboard-fill"></i> Nexus <span class="fs-6 text-muted ms-2 fw-normal">| Student</span>
        </span>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">
            <ul class="nav nav-underline nav-justify">
              <li class="nav-item">
                <router-link class="nav-link" :to="`/student/${studentId}`"><b>Dashboard</b></router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link" :to="`/student/${studentId}/applications`"
                  >Applications</router-link
                >
              </li>
            
              <li class="nav-item">
                <router-link class="nav-link" :to="`/student/${studentId}/placement-drives`"
                  >Placement Drives</router-link
                >
              </li>
            </ul>
          </ul>
          <form class="d-flex" role="search" @submit.prevent="handleSearch">
            <select v-model="searchType" class="form-select me-2" style="width: auto;">
              <option value="applications">Applications</option>
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
          <button class="btn btn-outline-primary ms-3" @click="router.push(`/student/${studentId}/profile`)">
            Profile
          </button>
          <button class="btn btn-outline-danger ms-3" @click="handleLogout">
            Logout
          </button>
        </div>
      </div>
    </nav>
    <div class="container mt-5">
      <router-view :key="$route.path" />
    </div>
  </div>
</template>