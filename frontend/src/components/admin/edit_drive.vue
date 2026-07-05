<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/services/api';

const route = useRoute();
const router = useRouter();

const loading = ref(true);
const error = ref('');
const successMessage = ref('');
const saving = ref(false);

const formData = ref({
    job_title: '',
    job_description: '',
    skills_required: '',
    min_cgpa: 0.0,
    working_experience_required: 0,
    deadline: '',
    salary: 0,
    status: ''
});

const driveId = route.params.id;

onMounted(async () => {
    try {
        const response = await api.get(`api/placement-drive/${driveId}`);
        const drive = response.data.drive;
        formData.value = {
            job_title: drive.job_title || '',
            job_description: drive.job_description || '',
            skills_required: drive.skills_required || '',
            min_cgpa: drive.min_cgpa || 0,
            working_experience_required: drive.working_experience_required || 0,
            deadline: drive.deadline || '',
            salary: drive.salary || 0,
            status: drive.status || 'pending'
        };
    } catch (err) {
        error.value = err.response?.data?.message || "Failed to load placement drive details.";
        console.error(err);
    } finally {
        loading.value = false;
    }
});

const submitForm = async () => {
    saving.value = true;
    error.value = '';
    successMessage.value = '';

    try {
        const response = await api.post(`api/placement-drive/${driveId}`, formData.value);
        successMessage.value = response.data.message || "Placement drive updated successfully!";
        setTimeout(() => {
            router.go(-1); // Go back to the previous page
        }, 1500);
    } catch (err) {
        error.value = err.response?.data?.message || "Failed to update placement drive.";
        console.error(err);
    } finally {
        saving.value = false;
    }
};

const cancel = () => {
    router.go(-1);
};
</script>

<template>
    <div class="container mt-5 mb-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="card shadow-sm">
                    <div class="card-header bg-primary text-white">
                        <h4 class="mb-0">Edit Placement Drive</h4>
                    </div>
                    <div class="card-body">
                        <!-- Loading State -->
                        <div v-if="loading" class="text-center py-4">
                            <div class="spinner-border text-primary" role="status">
                                <span class="visually-hidden">Loading...</span>
                            </div>
                            <p class="mt-2 text-muted">Loading drive details...</p>
                        </div>

                        <!-- Alerts -->
                        <div v-if="error" class="alert alert-danger" role="alert">
                            {{ error }}
                        </div>
                        <div v-if="successMessage" class="alert alert-success" role="alert">
                            {{ successMessage }}
                        </div>

                        <!-- Edit Form -->
                        <form v-if="!loading" @submit.prevent="submitForm">
                            <div class="mb-3">
                                <label class="form-label fw-bold">Job Title</label>
                                <input v-model="formData.job_title" type="text" class="form-control" required />
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-bold">Job Description</label>
                                <textarea v-model="formData.job_description" class="form-control" rows="4" required></textarea>
                            </div>

                            <div class="mb-3">
                                <label class="form-label fw-bold">Skills Required</label>
                                <input v-model="formData.skills_required" type="text" class="form-control" required placeholder="e.g., Python, Vue, SQL" />
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">Minimum CGPA</label>
                                    <input v-model.number="formData.min_cgpa" type="number" step="0.1" min="0" max="10" class="form-control" required />
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">Working Exp. Required (Years)</label>
                                    <input v-model.number="formData.working_experience_required" type="number" min="0" class="form-control" required />
                                </div>
                            </div>

                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">Salary (₹)</label>
                                    <input v-model.number="formData.salary" type="number" min="0" class="form-control" required />
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label fw-bold">Application Deadline</label>
                                    <input v-model="formData.deadline" type="date" class="form-control" required />
                                </div>
                            </div>

                            <div class="d-flex justify-content-end gap-2 mt-4">
                                <button type="button" class="btn btn-secondary" @click="cancel" :disabled="saving">Cancel</button>
                                <button type="submit" class="btn btn-primary" :disabled="saving">
                                    <span v-if="saving" class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
                                    Save Changes
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
.card {
    border: none;
    border-radius: 0.5rem;
}
.card-header {
    border-top-left-radius: 0.5rem !important;
    border-top-right-radius: 0.5rem !important;
}
</style>
