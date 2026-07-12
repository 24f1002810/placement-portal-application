<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import api from '@/services/api';

const router = useRouter();
const route = useRoute();

const activeDrives = ref([]);

const driveData = ref({
  job_title: '',
  job_description: '',
  skills_required: '',
  min_cgpa: '',
  working_experience_required: '',
  deadline: '',
  salary: ''
});

const isSubmitting = ref(false);
const error = ref('');

onMounted(async () => {
  try {
    const companyId = route.params.id;
    const response = await api.get(`/api/company/${companyId}/placement-drives`);
    if (response.data && response.data.placement_drives) {
      activeDrives.value = response.data.placement_drives.filter(
        drive => drive.status === 'pending' || drive.status === 'approved'
      );
    }
  } catch (err) {
    console.error("Failed to load company drives", err);
  }
});

const submitForm = async () => {
  isSubmitting.value = true;
  error.value = '';
  
  const jobTitle = driveData.value.job_title.trim().toLowerCase();
  const duplicate = activeDrives.value.find(
    drive => drive.job_title.trim().toLowerCase() === jobTitle
  );
  
  if (duplicate) {
    error.value = `An active placement drive for '${driveData.value.job_title}' already exists.`;
    isSubmitting.value = false;
    return;
  }
  
  try {
    const companyId = route.params.id;
    await api.post(`/api/company/${companyId}/placement-drives`, driveData.value);
    alert('Placement drive requested successfully! It is now pending admin approval.');
    router.push({ name: 'CompanyHome' });
  } catch (err) {
    error.value = err.response?.data?.message || 'Failed to submit placement drive request.';
    console.error('Error creating drive:', err);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
            <h4 class="mb-0">Request New Placement Drive</h4>
            <button class="btn btn-sm btn-outline-light" @click="router.back()">Back</button>
          </div>
          
          <div class="card-body">
            <div v-if="error" class="alert alert-danger" role="alert">
              {{ error }}
            </div>
            
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="job_title" class="form-label fw-bold">Job Title *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="job_title" 
                  v-model="driveData.job_title" 
                  required 
                  placeholder="e.g. Software Development Engineer"
                >
              </div>

              <div class="mb-3">
                <label for="job_description" class="form-label fw-bold">Job Description *</label>
                <textarea 
                  class="form-control" 
                  id="job_description" 
                  v-model="driveData.job_description" 
                  rows="4" 
                  required
                  placeholder="Describe the role and responsibilities..."
                ></textarea>
              </div>

              <div class="mb-3">
                <label for="skills_required" class="form-label fw-bold">Skills Required *</label>
                <input 
                  type="text" 
                  class="form-control" 
                  id="skills_required" 
                  v-model="driveData.skills_required" 
                  required
                  placeholder="e.g. Python, Vue.js, SQL"
                >
                <div class="form-text">Comma-separated list of skills.</div>
              </div>

              <div class="row mb-3">
                <div class="col-md-6">
                  <label for="min_cgpa" class="form-label fw-bold">Minimum CGPA *</label>
                  <input 
                    type="number" 
                    step="0.01" 
                    min="0" 
                    max="10" 
                    class="form-control" 
                    id="min_cgpa" 
                    v-model.number="driveData.min_cgpa" 
                    required
                    placeholder="e.g. 7.5"
                  >
                </div>
                <div class="col-md-6">
                  <label for="working_experience_required" class="form-label fw-bold">Required Experience (Years) *</label>
                  <input 
                    type="number" 
                    min="0"
                    class="form-control" 
                    id="working_experience_required" 
                    v-model.number="driveData.working_experience_required" 
                    required
                    placeholder="e.g. 0 for freshers"
                  >
                </div>
              </div>

              <div class="row mb-4">
                <div class="col-md-6">
                  <label for="salary" class="form-label fw-bold">Salary (₹) *</label>
                  <input 
                    type="number" 
                    min="0"
                    class="form-control" 
                    id="salary" 
                    v-model.number="driveData.salary" 
                    required
                    placeholder="e.g. 800000"
                  >
                </div>
                <div class="col-md-6">
                  <label for="deadline" class="form-label fw-bold">Application Deadline *</label>
                  <input 
                    type="date" 
                    class="form-control" 
                    id="deadline" 
                    v-model="driveData.deadline" 
                    required
                  >
                </div>
              </div>

              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary btn-lg" :disabled="isSubmitting">
                  <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                  Submit Request for Approval
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
