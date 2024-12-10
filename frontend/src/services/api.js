// frontend/src/services/api.js
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://127.0.0.1:5000/api',
    withCredentials: false,
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    },
});
const api = axios.create({
    baseURL: 'http://localhost:5000/api',
});
export default {
    getPublications() {
        return apiClient.get('/publications');
    },
    getPublication(id) {
        return apiClient.get(`/publications/${id}`);
    },
    getUsers() {
        return apiClient.get('/users');
    },
    login(credentials) {
        return apiClient.post('/login', credentials);
    },
    register(user) {
        return apiClient.post('/register', user);
    },
    updateUser(email, data) {
        return api.put(`/users/${email}`, data);
    },
    deleteUser(email) {
        return api.delete(`/users/${email}`);
    },
};
