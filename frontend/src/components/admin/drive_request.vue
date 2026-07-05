<script setup>
import { ref, onMounted } from "vue";
import api from "@/services/api";

const message = ref("");
const loading = ref(true);
const error = ref("");
const drives = ref(null);

onMounted(async () => {
    try {
        const response = await api.get("/api/drive-requests");
        drives.value = response.data.pending_drives;
    } catch (err) {
        error.value = err.response?.data?.message || "Failed to load dashboard";
        console.error("Dashboard error:", err);
    } finally {
        loading.value = false;
    }
});

const approveRequest = (requestId) => {
    // Implement API call to approve the registration request
    console.log("Approving request ID:", requestId);
    loading.value = true;
    error.value = "";
    api.post(`/api/drive-requests`, {'drive_id': requestId, 'action': 'approve'})
        .then((response) => {
            // Capture the success message from the API response
            message.value = response.data.message || "Request approved successfully";
            // Refresh the list of registration requests after approval
            return api.get("/api/drive-requests");
        })
        .then((response) => {
            drives.value = response.data.pending_drives;
        })
        .catch((err) => {
            error.value = err.response?.data?.message || "Failed to approve request";
            message.value = "";
            console.error("Approval error:", err);
        })
        .finally(() => {
            loading.value = false;
        });
};

const rejectRequest = (requestId) => {
    // Implement API call to reject the registration request
    console.log("Rejecting request ID:", requestId);
    loading.value = true;
    error.value = "";
    api.post(`/api/drive-requests`, {'drive_id': requestId, 'action': 'reject'})
        .then((response) => {
            // Capture the success message from the API response
            message.value = response.data.message || "Request rejected successfully";
            // Refresh the list of registration requests after rejection
            return api.get("/api/drive-requests");
        })
        .then((response) => {
            drives.value = response.data.pending_drives;
        })
        .catch((err) => {
            error.value = err.response?.data?.message || "Failed to reject request";
            message.value = "";
            console.error("Rejection error:", err);
        })
        .finally(() => {
            loading.value = false;
        });
};
</script>
<template>
    <div class="container">
        <h2 class="text-center">Drive Requests</h2>
        <div v-if="loading" class="loading">Loading...</div>
        <div v-else-if="error" class="error-alert alert-dismissible fade show" role="alert">
            {{ error }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        <div v-else-if="message" class="alert alert-success alert-dismissible fade show" role="alert">
            {{ message }}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
        
        <div v-if="drives && drives.length === 0" class="alert alert-info text-center">No Placement Drives are pending</div>
        <div v-else>
            <table class="table">
                <thead>
                    <tr>
                        <th>Company ID</th>
                        <th>Job Title</th>
                        <th>Deadline</th>
                        <th>Salary</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="drive in drives" :key="drive.id">
                        <td>{{ drive.company_id }}</td>
                        <td>{{ drive.job_title }}</td>
                        <td>{{ drive.deadline }}</td>
                        <td>{{ drive.salary }}</td>
                        <td>
                            <!-- Action buttons (e.g., Approve, Reject) can go here -->
                            <button class="btn btn-success btn-sm" @click="approveRequest(drive.id)">Approve</button>
                            <button class="btn btn-danger btn-sm" @click="rejectRequest(drive.id)">Reject</button>
                            <button class="btn btn-info btn-sm" @click="$router.push(`/placement-drive/${drive.id}`)">View Details</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>
<style scoped></style>