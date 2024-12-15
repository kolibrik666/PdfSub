<template>
  <div v-if="isReviewer">
    <div class="publications">
      <h1>For Review</h1>
      <!-- Displaying a list of publications -->
      <table>
        <thead>
        <tr>
          <th>Title</th>
          <th>Review Status</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="publication in filteredPublications" :key="publication._id">
          <td>
            <router-link :to="{ name: 'publication-detail', params: { id: publication._id } }">
              {{ publication.title }}
            </router-link>
          </td>
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
      <table>
        <thead>
        <tr>
          <th>Title</th>
          <th>Author</th>
          <th>Co-Authors</th>
          <th>Date of Submission</th>
          <th>Reviewer</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="publication in filteredPublications" :key="publication._id">
          <td>
            <router-link :to="{ name: 'publication-detail', params: { id: publication._id } }">
              {{ publication.title }}
            </router-link>
          </td>
          <td>{{ getUserName(publication.authorId) }}</td>
          <td>{{ publication.co_authors }}</td>
          <td>{{ publication.submit_status }}</td>
          <td>{{ getUserName(publication.reviewerId) || 'No reviewer assigned' }}</td>
       


          <td>


    
<select 
  v-model="selectedReviewer[publication._id]"
>
<option value=""  selected>Select Reviewer</option>

  <!-- List of all reviewers -->
    <option v-for="user in reviewers" :key="user._id" :value="user._id">
      {{ user.name }}
    </option>
</select>
          <button v-if="isAdmin && publication.review_status === 'pending'" @click="assignReviewer(publication)">Assign Reviewer</button>
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
      <table>
        <thead>
        <tr>
          <th>Title</th>
          <th>Author</th>
          <th>Co-Authors</th>
          <th>Date of Submission</th>
          <th>Actions</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="publication in filteredPublications" :key="publication._id">
          <td>
            <router-link :to="{ name: 'publication-detail', params: { id: publication._id } }">
              {{ publication.title }}
            </router-link>
          </td>
          <td>{{ getUserName(publication.authorId) }}</td>
          <td>{{ publication.co_authors }}</td>
          <td>{{ publication.submit_status }}</td>
          <td>
            <button v-if="isParticipant && isBeforeDeadline()" @click="submitPublication(publication)">Re-submit</button>
            <button @click="downloadPublication(publication.fileUrl)">Download</button>
          </td>
        </tr>
        </tbody>
      </table>

      <div v-if="isParticipant">
        <h2>Add Publication</h2>
        <form @submit.prevent="uploadPublication">
          <input type="text" v-model="newPublication.title" placeholder="Title" required />
          <input type="text" v-model="newPublication.authorId" placeholder="Author" required />
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
import { decodeTokenUpdateData } from '../services/tokenUtils';

export default {
  data() {
    return {
      user_id: '',
      publications: [],
      selectedReviewer: {}, // Tracks selected reviewer for each publication
      reviewers: [], // Store reviewers data here
      users: {}, // Store users data here
      newPublication: {
        title: '',
        authorId: '',
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
        return this.publications.filter(pub => pub.reviewerId === this.user_id);
      } else if (this.isParticipant) {
        return this.publications.filter(pub => pub.authorId === this.user_id);
      }
      return [];
    },
  },
  methods: {
    fetchPublications() {
      api.getPublications().then(response => {
        this.publications = response.data;
        const userIds = [...new Set(this.publications.flatMap(pub => [pub.authorId, pub.reviewerId]))];
        this.fetchUsers(userIds);
        this.fetchReviewers(); // Ensure reviewers list is populated

      });
    },
   
  fetchReviewers() {
    api.getUsers() // Or the endpoint to fetch users
      .then(response => {
        this.reviewers = response.data.filter(user => user.roles.isReviewer);
        console.log(this.reviewers); // Log the reviewers to check the list
      })
      .catch(error => {
        console.error('Error fetching reviewers:', error);
      });
  },
  async assignReviewer(publication) {
  const reviewerId = this.selectedReviewer[publication._id];
  
  if (!reviewerId) {
    alert("Please select a reviewer.");
    console.log("No reviewer selected for publication:", publication);
    return;
  }

  try {
    // 1. Make the API call to update the publication with the selected reviewer
    const publicationUpdateResponse = await api.updatePublication(publication._id, { reviewerId });

    console.log("Publication updated successfully:", publicationUpdateResponse);

    // 2. Update the local publication data for immediate UI update
    publication.reviewerId = reviewerId;

    // 3. You may want to reset the selected reviewer value for the UI
    this.selectedReviewer[publication._id] = ""; // Optionally reset the reviewer selection field

    alert("Reviewer updated successfully!");
  } catch (error) {
    console.error("Error assigning reviewer:", error);
    if (error.response) {
      console.error("Error response data:", error.response.data);
      console.error("Error response status:", error.response.status);
    } else {
      console.error("No response received from server.");
    }
    alert("An error occurred while assigning the reviewer. Please try again.");
  }
},

    fetchUsers(userIds) {
      Promise.all(userIds.map(id => api.getUserById(id).catch(() => null)))
        .then(responses => {
          responses.forEach(user => {
            if (user && user.data) {
              this.users[user.data._id] = `${user.data.name}`;
            }
          });
        })
        .catch(error => console.error("Failed to fetch users", error));
    },
    getUserName(userId) {
      return this.users[userId] || "Unknown";
    },
    setUserRole() {
      const token = localStorage.getItem('userToken');
      if (token) {
        decodeTokenUpdateData(token, this);
        this.isLoggedIn = true;
      }
    },
    submitPublication(publication) {
      if (this.isBeforeDeadline()) {
        publication.submit_status = 'submitted';
      } else {
        alert('Deadline has passed. You cannot submit the publication.');
      }
    },
    downloadPublication(fileUrl) {
      const link = document.createElement('a');
      link.href = fileUrl;
      link.download = fileUrl.split('/').pop();
      link.click();
    },
    isBeforeDeadline() {
      const deadline = new Date('2024-12-31');
      return new Date() <= deadline;
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