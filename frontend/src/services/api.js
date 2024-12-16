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
    addCommentToPublication(id, commentData) {
        return apiClient.post(`/publications/${id}/comments`, commentData);
    },
    updatePublication(id, data) {
        return apiClient.put(`/publications/${id}`, data);
    },
    deletePublication(id) {
        return apiClient.delete(`/publications/${id}`);
    },
    uploadPublication(formData) {
        return apiClient.post('/publications/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
    },
    getPublicationFile(fileId) {
        return apiClient.get(`/publications/file/${fileId}`, {
            responseType: 'blob', // Ensures the file is downloaded as a binary blob
        });
    },
    getUsers() {
        return apiClient.get('/users');
    },
    getUserById(id) {
        return apiClient.get(`/users/${id}`);
    },
    login(credentials) {
        return apiClient.post('/login', credentials);
    },
    register(user) {
        return apiClient.post('/register', user);
    },
    updateUser(email, data) {
        return apiClient.put(`/users/${email}`, data);
    },
    deleteUser(email) {
        return apiClient.delete(`/users/${email}`);
    },
    decode_token(data) {
        return apiClient.post('/decode-token', data);
    },
    submitReview(data) {
        return axios.post(`/reviews`, data); 
      },
 
};