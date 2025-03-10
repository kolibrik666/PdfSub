import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  withCredentials: false,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/json",
  },
});

export default {
  getPublications() {
    return apiClient.get("/publications");
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
  downloadPublication(fileId) {
    return apiClient.get(`/publications/file/${fileId}`, {
      responseType: "blob",
    });
  },
  uploadPublication(formData) {
    return apiClient.post("/publications/upload", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  },
  getUsers() {
    return apiClient.get("/users");
  },
  getUserById(id) {
    return apiClient.get(`/users/${id}`);
  },
  login(credentials) {
    return apiClient.post("/login", credentials);
  },
  register(user) {
    return apiClient.post("/register", user);
  },
  updateUser(id, data) {
    return apiClient.put(`/users/${id}`, data);
  },
  decode_token(data) {
    return apiClient.post("/decode-token", data);
  },
  createConference(conferenceData) {
    return apiClient.post("/conferences", conferenceData);
  },
  getConferences() {
    return apiClient.get("/conferences");
  },
  getConferenceDetails(id) {
    return apiClient.get(`/conferences/${id}`);
  },
  updateConference(id, data) {
    return apiClient.put(`/conferences/${id}`, data);
  },
  deleteConference(id) {
    return apiClient.delete(`/conferences/${id}`);
  },
};
