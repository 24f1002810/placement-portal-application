import api from '@/services/api';

const state = {
  user: JSON.parse(localStorage.getItem('user')) || null,
  token: localStorage.getItem('auth_token') || null,
  isAuthenticated: !!localStorage.getItem('auth_token'),
  isAdmin: JSON.parse(localStorage.getItem('user'))?.role === 'admin' || false,
  loading: false,
  error: null
};

const getters = {
  getUser: (state) => state.user,
  getToken: (state) => state.token,
  isAuthenticated: (state) => state.isAuthenticated,
  isAdmin: (state) => state.isAdmin,
  getUserRole: (state) => state.user?.role,
  getUserId: (state) => state.user?.id,
  getUserEmail: (state) => state.user?.email,
  getCompanyId: (state) => state.user?.companyId,
  getStudentId: (state) => state.user?.studentId,
  isLoading: (state) => state.loading,
  getError: (state) => state.error
};

const mutations = {
  SET_USER(state, user) {
    state.user = user;
    state.isAdmin = user?.role === 'admin';
    if (user) {
      localStorage.setItem('user', JSON.stringify(user));
    } else {
      localStorage.removeItem('user');
    }
  },
  SET_TOKEN(state, token) {
    state.token = token;
    state.isAuthenticated = !!token;
    if (token) {
      localStorage.setItem('auth_token', token);
    } else {
      localStorage.removeItem('auth_token');
    }
  },
  SET_IS_ADMIN(state, isAdmin) {
    state.isAdmin = isAdmin;
  },
  SET_LOADING(state, loading) {
    state.loading = loading;
  },
  SET_ERROR(state, error) {
    state.error = error;
  },
  CLEAR_USER(state) {
    state.user = null;
    state.token = null;
    state.isAuthenticated = false;
    state.isAdmin = false;
    localStorage.removeItem('user');
    localStorage.removeItem('auth_token');
  }
};

const actions = {
  async login({ commit }, credentials) {
    commit('SET_LOADING', true);
    commit('SET_ERROR', null);
    try {
      console.log("Attempting login with email:", credentials.email);

      const loginResponse = await api.post('/login?include_auth_token=true', {
        email: credentials.email,
        password: credentials.password,
      });

      console.log("Login response:", loginResponse.data);

      const token = loginResponse.data.response.user.authentication_token;
      console.log("Token received:", token);

      commit('SET_TOKEN', token);

      const dashboardResponse = await api.post('/api/dashboard');
      console.log("Dashboard response:", dashboardResponse.data);

      const userId = dashboardResponse.data.profile.id || dashboardResponse.data.profile.user_id;
      const userName = dashboardResponse.data.profile.name || dashboardResponse.data.profile.email;
      const userEmail = dashboardResponse.data.profile.email;
      const companyId = dashboardResponse.data.profile.company_id || null;
      const studentId = dashboardResponse.data.profile.student_id || null;
      const approvalStatus = dashboardResponse.data.profile.approval_status || null;
      const role = dashboardResponse.data.profile.role || 'student';

      const user = {
        id: userId,
        companyId: companyId,
        studentId: studentId,
        name: userName,
        email: userEmail,
        role: role,
        approval_status: approvalStatus
      };

      commit('SET_USER', user);
      commit('SET_IS_ADMIN', role === 'admin');

      return user;
    } catch (error) {
      console.error("Full error object:", error);
      console.error("Error response data:", error.response?.data);

      const errorMessage = error.response?.data?.response?.message ||
        error.response?.data?.message ||
        error.message ||
        'Login failed';
      commit('SET_ERROR', errorMessage);
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async register({ commit }, userData) {
    commit('SET_LOADING', true);
    commit('SET_ERROR', null);
    try {
      const response = await api.post('/register', userData);
      const { user, token } = response.data;

      commit('SET_USER', user);
      commit('SET_TOKEN', token);

      return { success: true, user };
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Registration failed';
      commit('SET_ERROR', errorMessage);
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async fetchUserProfile({ commit }) {
    commit('SET_LOADING', true);
    commit('SET_ERROR', null);
    try {
      const response = await api.get('/api/user/profile');
      const user = response.data.user;

      commit('SET_USER', user);
      commit('SET_IS_ADMIN', user.role === 'admin');

      return user;
    } catch (error) {
      const errorMessage = error.response?.data?.message || 'Failed to fetch user profile';
      commit('SET_ERROR', errorMessage);
      throw error;
    } finally {
      commit('SET_LOADING', false);
    }
  },

  async logout({ commit }) {
    try {
      await api.post('/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      commit('CLEAR_USER');
    }
  },

  updateUser({ commit }, user) {
    commit('SET_USER', user);
  },

  clearError({ commit }) {
    commit('SET_ERROR', null);
  },

  initializeAuth({ commit }) {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('user');

    if (token && user) {
      try {
        const parsedUser = JSON.parse(user);
        commit('SET_TOKEN', token);
        commit('SET_USER', parsedUser);
        commit('SET_IS_ADMIN', parsedUser.role === 'admin');
        console.log("Auth initialized from localStorage");
      } catch (error) {
        console.error("Invalid stored auth data:", error);
        commit('CLEAR_USER');
      }
    }
  },

  validateToken({ commit }) {
    const token = localStorage.getItem('auth_token');
    const user = localStorage.getItem('user');

    if (!token || !user) {
      commit('CLEAR_USER');
      return false;
    }

    try {
      JSON.parse(user);
      return true;
    } catch (error) {
      commit('CLEAR_USER');
      return false;
    }
  }
};

export default {
  namespaced: true,
  state,
  getters,
  mutations,
  actions
};
