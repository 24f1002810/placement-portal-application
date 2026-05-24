<script setup></script>

<template>
  <div class="home-container">
    <h1>Home</h1>
    <router-link to="/login" class="login-link">Login</router-link>
    <router-link to="/register" class="login-link" style="margin-left: 1rem"
      >Register</router-link
    >
  </div>
</template>

<style scoped>
.home-container {
  padding: 2rem;
  text-align: center;
}

h1 {
  color: #1f2937;
  margin-bottom: 2rem;
}

.login-link {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background-color: #3b82f6;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-weight: 600;
  transition: background-color 0.2s;
}

.login-link:hover {
  background-color: #2563eb;
}
</style>
