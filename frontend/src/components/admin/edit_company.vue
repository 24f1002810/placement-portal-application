<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/services/api";

const route = useRoute();
const router = useRouter();
const companyId = route.params.id;

const loading = ref(true);
const saving = ref(false);
const error = ref("");
const success = ref("");
const form = ref({
  name: "",
  email: "",
  hr_phone: "",
  website: "",
  location: "",
  description: "",
  approval_status: "",
  blocked: false,
});

onMounted(async () => {
  try {
    const response = await api.get(`/api/company/${companyId}`);
    const company = response.data.company || {};

    form.value = {
      name: company.name || "",
      email: company.email || "",
      hr_phone: company.hr_phone || "",
      website: company.website || "",
      location: company.location || "",
      description: company.description || "",
      approval_status: company.approval_status || "",
      blocked: company.active ?? false,
    };
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load company details";
    console.error("Load company error:", err);
  } finally {
    loading.value = false;
  }
});

async function submitForm() {
  saving.value = true;
  error.value = "";
  success.value = "";

  try {
    const payload = {
      name: form.value.name,
      hr_phone: form.value.hr_phone,
      website: form.value.website,
      location: form.value.location,
      description: form.value.description,
      approval_status: form.value.approval_status,
    };

    const response = await api.post(`/api/company/${companyId}`, payload);
    success.value = response.data.message || "Company details updated successfully.";

    setTimeout(() => {
      router.push({ name: "CompanyDetails", params: { id: companyId } });
    }, 600);
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to update company details";
    console.error("Update company error:", err);
  } finally {
    saving.value = false;
  }
}

function goBack() {
  router.push({ name: "CompanyDetails", params: { id: companyId } });
}
</script>

<template>
  <div class="container py-4">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        <div class="card shadow-sm">
          <div
            class="card-header bg-primary text-white d-flex justify-content-between align-items-center"
          >
            <div>
              <h4 class="mb-0">Edit Company Details</h4>
              <small class="text-light">Update company information</small>
            </div>
            <button class="btn btn-light btn-sm" @click="router.back()">Back</button>
          </div>

          <div class="card-body">
            <div v-if="loading" class="text-center py-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
            </div>

            <div v-else>
              <div v-if="error" class="alert alert-danger">{{ error }}</div>
              <div v-if="success" class="alert alert-success">{{ success }}</div>

              <form @submit.prevent="submitForm">
                <div class="row g-3">
                  <div class="col-md-6">
                    <label class="form-label">Company Name</label>
                    <input
                      v-model="form.name"
                      type="text"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Email</label>
                    <input
                      v-model="form.email"
                      type="email"
                      class="form-control"
                      disabled
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">HR Number</label>
                    <input
                      v-model="form.hr_phone"
                      type="text"
                      class="form-control"
                      required
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Location</label>
                    <input
                      v-model="form.location"
                      type="text"
                      class="form-control"
                      placeholder="e.g. New Yourk, USA"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Website</label>
                    <input
                      v-model="form.website"
                      type="url"
                      class="form-control"
                      placeholder="e.g. https://facebook.com"
                    />
                  </div>

                  <div class="col-md-6">
                    <label class="form-label">Description</label>
                    <input
                      v-model="form.description"
                      type="text"
                      class="form-control"
                      placeholder="e.g. A leading tech company that designs and manufactures GPUs"
                    />
                  </div>
                </div>

                <div class="d-flex justify-content-end gap-2 mt-4">
                  <button type="button" class="btn btn-outline-secondary" @click="router.back()">
                    Cancel
                  </button>
                  <button type="submit" class="btn btn-primary" :disabled="saving">
                    <span
                      v-if="saving"
                      class="spinner-border spinner-border-sm me-2"
                      role="status"
                    ></span>
                    {{ saving ? "Saving..." : "Save Changes" }}
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
