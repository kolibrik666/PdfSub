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
          <tr
            v-for="publication in reviewerPublications"
            :key="publication._id"
          >
            <td>
              <router-link
                :to="{
                  name: 'publication-detail',
                  params: { id: publication._id },
                }"
              >
                {{ publication.title }}
              </router-link>
            </td>
            <td>{{ publication.review_status }}</td>
            <td>
              <router-link
                :to="{ name: 'review', params: { id: publication._id } }"
              >
                <button
                  v-if="isReviewer && publication.review_status === 'pending'"
                >
                  Review
                </button></router-link
              >
              <button
                @click="
                  downloadPublication(
                    publication.fileId,
                    publication.title + '.pdf'
                  )
                "
              >
                Download
              </button>
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
          <tr v-for="publication in allPublications" :key="publication._id">
            <td>
              <router-link
                :to="{
                  name: 'publication-detail',
                  params: { id: publication._id },
                }"
              >
                {{ publication.title }}
              </router-link>
            </td>
            <td>{{ getUserName(publication.authorId) }}</td>
            <td>{{ publication.co_authors }}</td>
            <td>{{ publication.submissionDate }}</td>
            <td>
              {{
                getUserName(publication.reviewerId) || "No reviewer assigned"
              }}
            </td>
            <td>
              <select v-model="selectedReviewer[publication._id]">
                <!-- List of all reviewers -->
                <option
                  v-for="user in reviewers"
                  :key="user._id"
                  :value="user._id"
                >
                  {{ user.name }}
                </option>
              </select>
              <button
                v-if="isAdmin && publication.review_status === 'pending'"
                @click="assignReviewer(publication)"
              >
                Assign Reviewer
              </button>
              <button
                @click="
                  downloadPublication(
                    publication.fileId,
                    publication.title + '.pdf'
                  )
                "
              >
                Download
              </button>
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
          <tr
            v-for="publication in participantPublications"
            :key="publication._id"
          >
            <td>
              <router-link
                :to="{
                  name: 'publication-detail',
                  params: { id: publication._id },
                }"
              >
                {{ publication.title }}
              </router-link>
            </td>
            <td>{{ getUserName(publication.authorId) }}</td>
            <td>{{ publication.co_authors }}</td>
            <td>{{ publication.submissionDate }}</td>
            <td>
              <button
                v-if="isParticipant && isBeforeDeadline()"
                @click="deletePublication(publication)"
              >
                Delete
              </button>

              <button
                @click="
                  downloadPublication(
                    publication.fileId,
                    publication.title + '.pdf'
                  )
                "
              >
                Download file
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="isParticipant">
        <h2>Add Publication</h2>
        <form @submit.prevent="uploadPublication">
          <input
            type="text"
            v-model="newPublication.title"
            placeholder="Title"
            required
          />
          <input
            type="text"
            v-model="newPublication.co_authors"
            placeholder="Co-authors"
          />
          <input
            type="file"
            @change="handleFileUpload"
            accept=".pdf,.docx"
            required
          />
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
import api from "../services/api";
import { decodeTokenUpdateData } from "../services/tokenUtils";

export default {
  data() {
    return {
      user_id: "",
      publications: [],
      selectedReviewer: {},
      reviewers: [],
      users: {},
      newPublication: {
        title: "",
        authorId: "",
        selectedFile: null,
        co_authors: "",
        submissionDate: "",
        conferenceId: "",
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
    allPublications() {
      if (this.isAdmin) {
        return this.publications;
      }
      return [];
    },
    reviewerPublications() {
      if (this.isReviewer) {
        return this.publications.filter(
          (pub) => pub.reviewerId === this.user_id
        );
      }
      return [];
    },
    participantPublications() {
      if (this.isParticipant) {
        return this.publications.filter((pub) => pub.authorId === this.user_id);
      }
      return [];
    },
  },
  methods: {
    fetchPublications() {
      api.getPublications().then((response) => {
        this.publications = response.data;
        const userIds = [
          ...new Set(
            this.publications.flatMap((pub) => [pub.authorId, pub.reviewerId])
          ),
        ];
        this.fetchUsers(userIds);
        this.fetchReviewers(); 
      });
    },
    fetchReviewers() {
      api
        .getUsers() 
        .then((response) => {
          this.reviewers = response.data.filter(
            (user) => user.roles.isReviewer
          );
          console.log(this.reviewers); // Log the reviewers to check the list
        })
        .catch((error) => {
          console.error("Error fetching reviewers:", error);
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
        const publicationUpdateResponse = await api.updatePublication(
          publication._id,
          { reviewerId }
        );

        console.log(
          "Publication updated successfully:",
          publicationUpdateResponse
        );
        // 2. Update the local publication data for immediate UI update
        publication.reviewerId = reviewerId;

        // 3. Reset the selected reviewer value for the UI
        this.selectedReviewer[publication._id] = "";
        alert("Reviewer updated successfully!");
      } catch (error) {
        console.error("Error assigning reviewer:", error);
        if (error.response) {
          console.error("Error response data:", error.response.data);
          console.error("Error response status:", error.response.status);
        } else {
          console.error("No response received from server.");
        }
        alert(
          "An error occurred while assigning the reviewer. Please try again."
        );
      }
    },
    fetchUsers(userIds) {
      Promise.all(userIds.map((id) => api.getUserById(id).catch(() => null)))
        .then((responses) => {
          responses.forEach((user) => {
            if (user && user.data) {
              this.users[user.data._id] = `${user.data.name}`;
            }
          });
        })
        .catch((error) => console.error("Failed to fetch users", error));
    },
    getUserName(userId) {
      return this.users[userId] || "Unknown";
    },
    setUserRole() {
      const token = localStorage.getItem("userToken");
      if (token) {
        decodeTokenUpdateData(token, this);
        this.isLoggedIn = true;
      }
    },
    handleFileUpload(event) {
      this.newPublication.selectedFile = event.target.files[0]; // Store the selected file
    },
    async uploadPublication() {
      const formData = new FormData();
      formData.append("title", this.newPublication.title);
      formData.append("authorId", this.user_id);
      formData.append("co_authors", this.newPublication.co_authors);
      formData.append("file", this.newPublication.selectedFile);
      formData.append("conferenceId", this.newPublication.conferenceId);

      try {
        console.log("Uploading:", this.newPublication);
        await api.uploadPublication(formData);
        alert("Publication uploaded successfully!");
        this.newPublication = { title: "", authorId: "", selectedFile: null };
        this.uploadError = null;
      } catch (error) {
        this.uploadError = error.response?.data?.error || "Upload failed";
      }
    },
    async downloadPublication(fileId, filename) {
      console.log("Downloading publication:", fileId, filename);
      try {
        const response = await api.downloadPublication(fileId);
        const blob = new Blob([response.data], {
          type: response.headers["content-type"],
        });
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = filename;
        document.body.appendChild(link);
        link.click();

        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
      } catch (error) {
        console.error("Error downloading publication:", error.message);
        alert("An error occurred while downloading the file.");
      }
    },
    async deletePublication(publication) {
      try {
        const confirmation = window.confirm(
          `Are you sure you want to delete the publication titled "${publication.title}"?`
        );

        if (!confirmation) return;

        await api.deletePublication(publication._id);

        // Update the local list by filtering out the deleted publication
        this.publications = this.publications.filter(
          (pub) => pub._id !== publication._id
        );

        alert("Publication deleted successfully!");
      } catch (error) {
        console.error("Error deleting publication:", error);
        alert("An error occurred while deleting the publication.");
      }
    },
    isBeforeDeadline() {
      const deadline = new Date("2024-12-31");
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

th,
td {
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
