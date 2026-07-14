<script setup>
</script>

<template>
  <div class="landing-page bg-light min-vh-100 d-flex flex-column">
    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3">
      <div class="container">
        <a class="navbar-brand fw-bold text-primary fs-3 d-flex align-items-center gap-2" href="#">
          <i class="bi bi-mortarboard-fill"></i> Nexus
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav align-items-center gap-3">
            <li class="nav-item">
              <router-link to="/login" class="nav-link fw-medium text-dark btn btn-link text-decoration-none px-3">Log In</router-link>
            </li>
            <li class="nav-item">
              <router-link to="/register" class="btn btn-primary fw-semibold px-4 rounded-pill shadow-sm">Get Started</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section flex-grow-1 d-flex align-items-center py-5">
      <div class="container">
        <div class="row align-items-center g-5">
          <div class="col-lg-6 text-center text-lg-start">
            <span class="badge bg-primary-subtle text-primary rounded-pill px-3 py-2 mb-3 fw-medium">
              University Placement Portal
            </span>
            <h1 class="display-4 fw-extrabold text-dark mb-4 lh-tight">
              Connect with Top Companies, Land Your <span class="text-primary">Dream Job</span>
            </h1>
            <p class="lead text-secondary mb-5 pe-lg-4 lh-base">
              The ultimate platform bridging the gap between talented students and industry-leading organizations. Streamline your placement process today.
            </p>
            <div class="d-flex flex-column flex-sm-row gap-3 justify-content-center justify-content-lg-start">
              <router-link to="/register" class="btn btn-primary btn-lg rounded-pill px-5 py-3 fw-semibold shadow-sm d-flex align-items-center justify-content-center gap-2">
                Join Now <i class="bi bi-arrow-right"></i>
              </router-link>
              <router-link to="/login" class="btn btn-outline-dark btn-lg rounded-pill px-5 py-3 fw-semibold">
                Sign In
              </router-link>
            </div>
          </div>
          <div class="col-lg-6 text-center">
            <div class="position-relative">
              <div class="blob-shape bg-primary opacity-10 position-absolute top-50 start-50 translate-middle w-100 h-100 rounded-circle filter-blur z-n1"></div>
              <img src="/hero_illustration.png" alt="Placement Portal Illustration" class="img-fluid floating-img drop-shadow w-100" style="max-width: 600px;">
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="bg-white py-5 py-lg-7">
      <div class="container py-5">
        <div class="text-center mb-5 pb-3">
          <h2 class="fw-bold text-dark mb-3">Designed for Everyone</h2>
          <p class="text-muted mx-auto" style="max-width: 600px;">Our platform provides a seamless experience for all stakeholders in the university placement ecosystem.</p>
        </div>
        
        <div class="row g-4">
          <!-- Student Feature -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm feature-card p-4 rounded-4 bg-light">
              <div class="icon-box bg-primary text-white rounded-circle d-flex align-items-center justify-content-center mb-4 shadow-sm" style="width: 60px; height: 60px;">
                <i class="bi bi-person-fill fs-3"></i>
              </div>
              <h4 class="fw-bold mb-3">For Students</h4>
              <p class="text-muted mb-0">Create your profile, discover exciting placement drives, and track your applications in real-time. Your next big career move starts here.</p>
            </div>
          </div>
          
          <!-- Company Feature -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm feature-card p-4 rounded-4 bg-light">
              <div class="icon-box bg-success text-white rounded-circle d-flex align-items-center justify-content-center mb-4 shadow-sm" style="width: 60px; height: 60px;">
                <i class="bi bi-building fs-3"></i>
              </div>
              <h4 class="fw-bold mb-3">For Companies</h4>
              <p class="text-muted mb-0">Post opportunities, review applicant profiles seamlessly, and hire the brightest minds directly from the campus.</p>
            </div>
          </div>
          
          <!-- Admin Feature -->
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow-sm feature-card p-4 rounded-4 bg-light">
              <div class="icon-box bg-dark text-white rounded-circle d-flex align-items-center justify-content-center mb-4 shadow-sm" style="width: 60px; height: 60px;">
                <i class="bi bi-shield-lock-fill fs-3"></i>
              </div>
              <h4 class="fw-bold mb-3">For University Admins</h4>
              <p class="text-muted mb-0">Oversee the entire placement process, manage company approvals, and gain valuable insights through detailed statistics.</p>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- Footer -->
    <footer class="bg-dark text-white py-4 mt-auto">
      <div class="container text-center">
        <p class="mb-0 opacity-75 small">&copy; 2026 Nexus Placement Portal. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
@import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css");

.fw-extrabold {
  font-weight: 800;
}

.lh-tight {
  line-height: 1.2;
}

.filter-blur {
  filter: blur(60px);
}

.drop-shadow {
  filter: drop-shadow(0 20px 30px rgba(0,0,0,0.1));
}

.floating-img {
  animation: float 6s ease-in-out infinite;
}

.feature-card {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 1rem 3rem rgba(0,0,0,0.1) !important;
  background-color: white !important;
}

.py-lg-7 {
  @media (min-width: 992px) {
    padding-top: 6rem !important;
    padding-bottom: 6rem !important;
  }
}

@keyframes float {
  0% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
  100% {
    transform: translateY(0px);
  }
}
</style>
