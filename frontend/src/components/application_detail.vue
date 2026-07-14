<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useStore } from 'vuex';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();
const store = useStore();

const application = ref(null);
const loading = ref(true);
const error = ref('');
const isProcessing = ref(false);
const editStatus = ref('');
const editInterviewDate = ref('');

const isCompanyOrAdmin = store.getters['user/isAdmin'] || store.getters['user/getUserRole'] === 'company';
const role = store.getters['user/getUserRole'];

onMounted(async () => {
  await fetchApplication();
});

const fetchApplication = async () => {
  loading.value = true;
  try {
    const res = await api.get(`/api/application/${route.params.id}`);
    application.value = res.data.application;
    editStatus.value = application.value.status;
    editInterviewDate.value = application.value.interview_date ? application.value.interview_date.split('T')[0] : '';
  } catch (err) {
    error.value = 'Failed to load application details.';
    console.error('Error fetching application:', err);
  } finally {
    loading.value = false;
  }
};

const updateStatus = async () => {
  isProcessing.value = true;
  try {
    await api.post(`/api/application/${route.params.id}`, { 
        status: editStatus.value,
        interview_date: editInterviewDate.value || null
    });
    application.value.status = editStatus.value;
    application.value.interview_date = editInterviewDate.value;
    alert('Application updated successfully.');
  } catch (err) {
    alert('Failed to update status.');
    console.error('Error updating status:', err);
  } finally {
    isProcessing.value = false;
  }
};

const respondToOffer = async (newStatus) => {
  const confirmMsg = newStatus === 'placed' 
    ? "Are you sure you want to accept this offer?" 
    : "Are you sure you want to reject this offer?";
    
  if (confirm(confirmMsg)) {
    isProcessing.value = true;
    try {
      await api.post(`/api/application/${route.params.id}`, { 
          status: newStatus
      });
      application.value.status = newStatus;
      alert(`Offer ${newStatus === 'placed' ? 'accepted' : 'rejected'} successfully.`);
    } catch (err) {
      alert('Failed to respond to offer.');
      console.error('Error responding to offer:', err);
    } finally {
      isProcessing.value = false;
    }
  }
};

const getStatusBadgeClass = (status) => {
  switch (status) {
    case 'applied': return 'badge bg-primary';
    case 'shortlisted': return 'badge bg-info text-dark';
    case 'selected (for interview)': return 'badge bg-warning text-dark';
    case 'offered': return 'badge bg-success';
    case 'placed': return 'badge bg-success';
    case 'rejected': return 'badge bg-danger';
    default: return 'badge bg-secondary';
  }
};

const formatDate = (dateString) => {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleDateString();
};
</script>

<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Application Details</h2>
      <button class="btn btn-outline-secondary" @click="router.back()">Back</button>
    </div>

    <div v-if="loading" class="text-center mt-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else-if="application" class="row">
      <div class="col-md-6 mb-4">
        <div class="card shadow-sm h-100 border-0">
          <div class="card-header bg-primary text-white">
            <h5 v-if="isCompanyOrAdmin" class="mb-0">Applicant Details</h5>
            <h5 v-else class="mb-0">Your Details</h5>
          </div>
          <div class="card-body">
            <h4 class="card-title">{{ application.student_details.name }}</h4>
            <hr />
            <dl class="row mb-0">
              <dt class="col-sm-4">Email</dt>
              <dd class="col-sm-8">{{ application.student_details.email }}</dd>
              
              <dt class="col-sm-4">Phone</dt>
              <dd class="col-sm-8">{{ application.student_details.phone_number }}</dd>
              
              <dt class="col-sm-4">CGPA</dt>
              <dd class="col-sm-8">{{ application.student_details.cgpa }}</dd>
              
              <dt class="col-sm-4">Education</dt>
              <dd class="col-sm-8">{{ application.student_details.education || 'N/A' }}</dd>
              
              <dt class="col-sm-4">Skills</dt>
              <dd class="col-sm-8">
                <span v-for="skill in application.student_details.skills" :key="skill" class="badge bg-secondary me-1">
                  {{ skill }}
                </span>
              </dd>
            </dl>
          </div>
        </div>
      </div>

      <div class="col-md-6 mb-4">
        <div class="card shadow-sm h-100 border-0">
          <div class="card-header bg-secondary text-white">
            <h5 class="mb-0">Placement Drive Details</h5>
          </div>
          <div class="card-body">
            <h4 class="card-title">{{ application.drive_details.job_title }}</h4>
            <h6 class="card-subtitle mb-3 text-muted">{{ application.drive_details.company_name }}</h6>
            <hr />
            <dl class="row mb-0">
              <dt class="col-sm-4">Min CGPA</dt>
              <dd class="col-sm-8">{{ application.drive_details.min_cgpa }}</dd>
              
              <dt class="col-sm-4">Salary</dt>
              <dd class="col-sm-8">₹{{ application.drive_details.salary }}</dd>
              
              <dt class="col-sm-4">Deadline</dt>
              <dd class="col-sm-8">{{ formatDate(application.drive_details.deadline) }}</dd>
              
              <dt class="col-sm-12 mt-2">Job Description</dt>
              <dd class="col-sm-12">{{ application.drive_details.job_description }}</dd>
            </dl>
          </div>
        </div>
      </div>

      <div class="col-12 mb-4">
        <div class="card shadow-sm border-0">
          <div class="card-header bg-info text-dark">
            <h5 class="mb-0">Application Status</h5>
          </div>
          <div class="card-body d-flex justify-content-between align-items-center">
            <div>
              <span class="fs-5 fw-bold me-3">Current Status:</span>
              <span :class="getStatusBadgeClass(application.status) + ' fs-5 px-3 py-2 text-capitalize'">
                {{ application.status }}
              </span>
              <div v-if="application.interview_date" class="mt-2 text-muted">
                 <strong>Interview Date:</strong> {{ formatDate(application.interview_date) }}
              </div>
            </div>
            
            <div v-if="isCompanyOrAdmin" class="d-flex align-items-center gap-2">
              <select class="form-select w-auto" v-model="editStatus">
                <option value="applied">Applied</option>
                <option value="shortlisted">Shortlisted</option>
                <option value="selected">Select for Interview</option>
                <option value="offered">Offer Letter</option>
                <option v-if="role == 'admin'" value="placed">Placed</option>
                <option v-if="role == 'admin'" value="rejected">Rejected</option>
              </select>
              <input type="date" class="form-control w-auto" v-model="editInterviewDate" title="Interview Date (if applicable)" />
              <button 
                @click="updateStatus()" 
                :disabled="isProcessing"
                class="btn btn-primary">
                Save Changes
              </button>
            </div>

            <div v-if="role === 'student' && application.status === 'offered'" class="d-flex align-items-center gap-2">
               <button @click="respondToOffer('placed')" :disabled="isProcessing" class="btn btn-success">Accept Offer</button>
               <button @click="respondToOffer('rejected')" :disabled="isProcessing" class="btn btn-danger">Reject Offer</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
