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
};