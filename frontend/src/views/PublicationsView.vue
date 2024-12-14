<template>
  <div class="publications">
    <h1>Publications</h1>

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
      <tr v-for="publication in filteredPublications" :key="publication.id">
        <td>
          <router-link :to="{ name: 'publication-detail', params: { id: publication.id } }">
            {{ publication.title }}
          </router-link>
        </td>
        <td>{{ publication.authors.join(', ') }}</td>
        <td>{{ publication.status }}</td>
        <td>
          <!-- Actions based on role -->
          <button v-if="isAdmin && publication.status === 'drafted'" @click="editPublication(publication)">Edit</button>
          <button v-if="isAdmin && publication.status === 'drafted'" @click="deletePublication(publication.id)">Delete</button>
          <button v-if="(isAdmin || isReviewer) && publication.status !== 'submitted'" @click="submitPublication(publication)">Submit</button>
          <button @click="downloadPublication(publication.fileUrl)">Download</button>
        </td>
      </tr>
      </tbody>
    </table>

    <!-- Upload New Publication (only for students) -->
    <div v-if="isParticipant">
      <h2>Upload New Publication</h2>
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
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      publications: [
        { id: 1, title: 'Publication 1', authors: ['Student 1'], status: 'drafted', fileUrl: 'path/to/publication1.pdf' },
        { id: 2, title: 'Publication 2', authors: ['Student 2'], status: 'submitted', fileUrl: 'path/to/publication2.pdf' },
        // Add more dummy publications as needed
      ],
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
        return this.publications.filter(pub => pub.status !== 'drafted');
      } else if (this.isParticipant) {
        return this.publications.filter(pub => pub.authors.includes('Student 1')); // Example filter for student
      }
      return [];
    },
  },
  methods: {
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
        publication.status = 'submitted';
        console.log(`Publication ${publication.title} submitted.`);
      } else {
        alert('Deadline has passed. You cannot submit the publication.');
      }
    },
    editPublication(publication) {
      console.log(`Editing publication ${publication.title}`);
    },
    deletePublication(publicationId) {
      console.log(`Deleting publication with ID: ${publicationId}`);
      this.publications = this.publications.filter(pub => pub.id !== publicationId);
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
        status: 'drafted',
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