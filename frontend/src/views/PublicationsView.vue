<template>
<div v-if="isReviewer">
  <div class="publications">
    <h1>For Review</h1>
    <!-- Displaying a list of publications -->
    <table>
      <thead>
      <tr>
        <th>Title</th>
        <th>Authors</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="publication in publications" :key="publication._id">
        
        <td>
          <router-link :to="{ name: 'publication-detail', params: { id: publication._id } }">
            {{ publication.title }}
          </router-link>
        </td>

        <td>{{ publication.authors.join(", ") }}</td>
        <td>{{ publication.review_status }}</td>
        
        <td>
          <button v-if="isReviewer && publication.review_status === 'pending'" @click="editPublication(publication)">Review</button>
          <button @click="downloadPublication(publication.fileUrl)">Download</button>
        </td>
      
      </tr>
      </tbody>
    </table>

  </div>
  </div>

<div v-if="isAdmin">
  <div class="publications">
    <h1>Assign Reviewer</h1>
    <!-- Displaying a list of publications -->
    <table>
      <thead>
      <tr>
        <th>Title</th>
        <th>Authors</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="publication in publications" :key="publication._id">

        <td>
          <router-link :to="{ name: 'publication-detail', params: { id: publication._id } }">
            {{ publication.title }}
          </router-link>
        </td>
        <td>{{ publication.authors.join(", ") }}</td>
        <td>{{ publication.submit_status }}</td>
        <td>
          <button v-if="(isAdmin) && publication.submit_status.includes('submitted') && publication.review_status === 'pending'" @click="assignReviewer(publication)">Assign Reviewer</button>
          <button @click="downloadPublication(publication.fileUrl)">Download</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
  </div>
  <div v-if="isParticipant">
  <div class="publications">
    <h1>My Publications</h1>
    <!-- Displaying a list of publications -->
    <table>
      <thead>
      <tr>
        <th>Title</th>
        <th>Authors</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="publication in publications" :key="publication._id">
        <td>
          <router-link :to="{ name: 'publication-detail', params: { id: publication._id } }">
            {{ publication.title }}
          </router-link>
        </td>
        <td>{{ publication.authors.join(", ") }}</td>
        <td>{{ publication.submit_status }}</td>
        <td>
  <button 
    v-if="isParticipant && !isPastDeadline('2024-12-30T23:59:59Z')" 
    @click="submitPublication(publication)">
    Re-submit
  </button>
  <button @click="downloadPublication(publication.fileUrl)">Download</button>
</td>
      </tr>
      </tbody>
    </table>

    <!-- Upload New Publication (only for students) -->
    <div v-if="isParticipant">
      <h2>Add Publication</h2>
      <form @submit.prevent="uploadPublication">
        <input type="text" v-model="newPublication.title" placeholder="Title" required />
        <input type="text" v-model="newPublication.authors" placeholder="Authors (comma separated)" required />
        <input type="file" @change="handleFileUpload" accept=".pdf,.docx" required />
        <button type="submit">Upload</button>
      </form>
      <div v-if="uploadError" class="error-message">
        <p>{{ uploadError }}</p>
      </div>
    </div>
  </div>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      publications: [],
      newPublication: {
        title: '',
        authors: '',
        file: null,
      },
      uploadError: null,
      isLoggedIn: false,
      isAdmin: false,
      isParticipant: false,
      isReviewer: false,
    };
  },
  created() {
    this.setUserRole();
  },
  computed: {
    filteredPublications() {
      if (this.isAdmin) {
        return this.publications;
      } else if (this.isReviewer) {
        return this.publications.filter(pub => pub.submit_status !== 'drafted');
      } else if (this.isParticipant) {
        return this.publications.filter(pub => pub.authors.includes('Student 1')); // Example filter for student
      }
      return [];
    },
  },
  methods: {
    fetchPublications() {
      api.getPublications().then(response => {
        this.publications = response.data;
      });
    },
    setUserRole() {
      const token = localStorage.getItem('userToken');
      if (token) {
        this.decodeTokenUpdateData(token);
      }
    },
    decodeTokenUpdateData(token) {
      api.decode_token({ token })
          .then(response => {
            const decodedToken = response.data.user;
            this.isAdmin = decodedToken.isAdmin;
            this.isParticipant = decodedToken.isParticipant;
            this.isReviewer = decodedToken.isReviewer;
            this.isLoggedIn = true;
          })
          .catch(error => {
            console.error("Token decoding failed", error.response ? error.response.data : error.message);
            alert("Token decoding failed: " + (error.response ? error.response.data : error.message));
          });
    },
    submitPublication(publication) {
      if (this.isBeforeDeadline()) {
        publication.submit_status = 'submitted';
        console.log(`Publication ${publication.title} submitted.`);
      } else {
        alert('Deadline has passed. You cannot submit the publication.');
      }
    },
    isPastDeadline(deadline) {
    if (!deadline) return false; // If no deadline, allow submission
    const now = new Date(); // Get the current date and time
    const deadlineDate = new Date(deadline); // Convert deadline to a Date object
    return now > deadlineDate; // Check if the current date is past the deadline
  },
    handleFileUpload(event) {
      this.newPublication.file = event.target.files[0];
    },
    uploadPublication() {
      if (!this.newPublication.file) {
        this.uploadError = 'Please select a file to upload.';
        return;
      }
      const newPub = {
        ...this.newPublication,
        id: this.publications.length + 1,
        submit_status: 'drafted',
        fileUrl: URL.createObjectURL(this.newPublication.file),
      };
      this.publications.push(newPub);
      this.newPublication = { title: '', authors: '', file: null };
      this.uploadError = null;
    },
    downloadPublication(fileUrl) {
      const link = document.createElement('a');
      link.href = fileUrl;
      link.download = fileUrl.split('/').pop();
      link.click();
    },
    isBeforeDeadline() {
      const deadline = new Date('2024-12-31');
      const currentDate = new Date();
      return currentDate <= deadline;
    },
  },
  mounted() {
    this.fetchPublications();
  },
};
</script>

<style scoped>
.publications {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
}

th {
  background-color: #f2f2f2;
}

button {
  margin-right: 5px;
}

form {
  margin-top: 20px;
}

input[type="text"] {
  display: block;
  margin-bottom: 10px;
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

input[type="file"] {
  display: block;
  margin-bottom: 10px;
}

button[type="submit"] {
  padding: 10px 20px;
}

.error-message {
  color: red;
  margin-top: 20px;
}
</style>