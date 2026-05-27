import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

api.interceptors.request.use((config) => {
    // Don't send token for login endpoints
    if (!config.url.includes('/login')) {
        const token = localStorage.getItem('auth_token');
        if (token) {
            config.headers['Authentication-Token'] = token;
        }
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default api;