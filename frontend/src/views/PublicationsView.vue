<template>
  <div v-if="isReviewer">
    <div class="publications">
      <h1>For Review</h1>
      <PublicationsFilter :conferences="conferencesList" :initialFilters="{
        query: filterQuery,
        status: filterStatus,
        conference: filterConference,
      }" @filter-change="updateFilters" />
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Review Deadline</th>
            <th>Review Status</th>
            <th>Conference</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="publication in filteredReviewerPublications" :key="publication._id">
            <td>
              <router-link :to="{
                name: 'publication-detail',
                params: { id: publication._id },
              }">
                {{ publication.title }}
              </router-link>
            </td>
            <td>
              {{ getConferencePaperReviewDeadline(publication.conferenceId) }}
            </td>
            <td>{{ publication.review_status }}</td>
            <td>
              {{ getConferenceName(publication.conferenceId) }}
            </td>
            <td>
              <router-link :to="{ name: 'review', params: { id: publication._id } }">
                <button :disabled="!(
                    isReviewer &&
                    new Date(
                      getConferencePaperReviewDeadline(
                        publication.conferenceId
                      )
                    ).getTime() > new Date().getTime()
                  )
                  ">
                  Review
                </button>
              </router-link>
              <button class="download-button" @click="
                downloadPublication(
                  publication.fileId,
                  publication.title + '.pdf'
                )
                ">
                <i class="fa-solid fa-file-arrow-down"></i> Download
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>

  <div v-if="isAdmin">
    <div class="publications">
      <h1>All Publications</h1>
      <PublicationsFilter :conferences="conferencesList" :initialFilters="{
        query: filterQuery,
        status: filterStatus,
        conference: filterConference,
      }" @filter-change="updateFilters" />
      <button @click="downloadPublications('filtered')" id="downloadSelectedPublicationsBtn">
        <i class="fa-regular fa-file-zipper"></i> Download Filtered Publications
      </button>
      <button @click="downloadPublications('selected')" id="downloadSelectedPublicationsBtn">
        <i class="fa-regular fa-file-zipper"></i> Download Selected Publications
      </button>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Co-Authors</th>
            <th>Date of Submission</th>
            <th>Review Status</th>
            <th>Conference</th>
            <th>Reviewer</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="publication in filteredAllPublications" :key="publication._id">
            <td>
              <router-link :to="{
                name: 'publication-detail',
                params: { id: publication._id },
              }">
                {{ publication.title }}
              </router-link>
            </td>
            <td>{{ getUserName(publication.authorId) }}</td>
            <td>{{ publication.co_authors }}</td>
            <td>{{ publication.submissionDate }}</td>
            <td>{{ publication.review_status }}</td>
            <td>
              <select v-model="publication.conferenceId" @change="
                updateConference(publication._id, publication.conferenceId)
                ">
                <option v-for="conference in conferences" :key="conference._id" :value="conference._id">
                  {{ conference.name }}
                </option>
              </select>
            </td>
            <td>
              <select v-model="publication.reviewerId" @change="assignReviewer(publication)"
                :disabled="publication.review_status !== 'pending'">
                <option v-for="user in reviewers" :key="user._id" :value="user._id">
                  {{ user.name }}
                </option>
              </select>
              <span v-if="!publication.reviewerId">Reviewer not selected</span>
            </td>
            <td>
              <input type="checkbox" v-model="selectedPublications" :value="publication._id" class="custom-checkbox" />
              <button class="download-button" @click="
                downloadPublication(
                  publication.fileId,
                  publication.title + '.pdf'
                )
                ">
                <i class="fa-solid fa-file-arrow-down"></i> Download
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
      <PublicationsFilter :conferences="conferencesList" :initialFilters="{
        query: filterQuery,
        status: filterStatus,
        conference: filterConference,
      }" @filter-change="updateFilters" />
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Co-Authors</th>
            <th>Date of Submission</th>
            <th>Conference</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="publication in filteredParticipantPublications" :key="publication._id">
            <td>
              <router-link :to="{
                name: 'publication-detail',
                params: { id: publication._id },
              }">
                {{ publication.title }}
              </router-link>
            </td>
            <td>{{ getUserName(publication.authorId) }}</td>
            <td>{{ publication.co_authors }}</td>
            <td>{{ publication.submissionDate }}</td>
            <td>{{ getConferenceName(publication.conferenceId) }}</td>
            <td>
              <button class="download-button" @click="
                downloadPublication(
                  publication.fileId,
                  publication.title + '.pdf'
                )
                ">
                <i class="fa-solid fa-file-arrow-down"></i> Download
              </button>
              <button :disabled="!isBeforeDeadline(publication.conferenceId)" @click="deletePublication(publication)">
                <i class="fa-regular fa-trash-can"></i> Delete
              </button>
            </td>
          </tr>
        </tbody>
      </table>

      <div v-if="isParticipant">
        <h2>Add Publication</h2>
        <form @submit.prevent="uploadPublication">
          <input type="text" v-model="newPublication.title" placeholder="Title" required />
          <input type="text" v-model="newPublication.co_authors" placeholder="Co-authors" />
          <input type="text" v-model="newPublication.key_words" placeholder="Keywords" />
          <select v-model="newPublication.conferenceId">
            <option value="" disabled>Select a conference</option>
            <option v-for="conference in inProgressConferences" :key="conference._id" :value="conference._id">
              {{ conference.name }}
            </option>
          </select>
          <input type="file" @change="handleFileUpload" ref="fileInput" accept=".pdf" required />
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
import PublicationsFilter from "@/components/PublicationsFilter.vue";
import JSZip from "jszip";

export default {
  components: { PublicationsFilter },
  data() {
    return {
      user_id: "",
      publications: [],
      selectedPublications: [],
      reviewers: [],
      users: {},
      conferences: {},
      newPublication: {
        title: "",
        authorId: "",
        selectedFile: null,
        co_authors: "",
        key_words: "",
        submissionDate: "",
        conferenceId: "",
      },
      filterQuery: "",
      filterStatus: "",
      filterConference: "",
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
    filteredReviewerPublications() {
      return this.reviewerPublications.filter((publication) => {
        const matchesTitle = publication.title
          .toLowerCase()
          .includes(this.filterQuery.toLowerCase());
        const matchesStatus =
          !this.filterStatus || publication.review_status === this.filterStatus;
        const matchesConference =
          !this.filterConference ||
          publication.conferenceId === this.filterConference;
        return matchesTitle && matchesStatus && matchesConference;
      });
    },
    filteredAllPublications() {
      return this.publications.filter((publication) => {
        const matchesTitle = publication.title
          .toLowerCase()
          .includes(this.filterQuery.toLowerCase());
        const matchesStatus =
          !this.filterStatus || publication.review_status === this.filterStatus;
        const matchesConference =
          !this.filterConference ||
          publication.conferenceId === this.filterConference;
        return matchesTitle && matchesStatus && matchesConference;
      });
    },
    filteredParticipantPublications() {
      return this.participantPublications.filter((publication) => {
        const matchesTitle = publication.title
          .toLowerCase()
          .includes(this.filterQuery.toLowerCase());
        const matchesStatus =
          !this.filterStatus || publication.review_status === this.filterStatus;
        const matchesConference =
          !this.filterConference ||
          publication.conferenceId === this.filterConference;
        return matchesTitle && matchesStatus && matchesConference;
      });
    },
    conferencesList() {
      return Object.values(this.conferences);
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
    inProgressConferences() {
      const currentDate = new Date();
      return Object.values(this.conferences).filter((conference) => {
        const startDate = new Date(conference.start_date);
        const endDate = new Date(conference.end_date);
        return currentDate >= startDate && currentDate <= endDate;
      });
    },
  },
  methods: {
    updateFilters(filters) {
      this.filterQuery = filters.query;
      this.filterStatus = filters.status;
      this.filterConference = filters.conference;
    },
    fetchPublications() {
      api.getPublications().then((response) => {
        this.publications = response.data;
        const userIds = [
          ...new Set(
            this.publications.flatMap((pub) => {
              const ids = [pub.authorId];
              if (pub.reviewerId && pub.reviewerId.trim() !== "") {
                ids.push(pub.reviewerId);
              }
              return ids;
            })
          ),
        ];
        this.fetchUsers(userIds);
        this.fetchReviewers();
        this.fetchConferences();
      });
    },
    fetchReviewers() {
      api
        .getUsers()
        .then((response) => {
          this.reviewers = response.data.filter(
            (user) => user.roles.isReviewer
          );
        })
        .catch((error) => {
          console.error("Error fetching reviewers:", error);
        });
    },
    fetchConferences() {
      api
        .getConferences()
        .then((response) => {
          this.conferences = response.data.reduce((acc, conf) => {
            acc[conf._id] = conf;
            return acc;
          }, {});
        })
        .catch((error) => {
          console.error("Error fetching conferences:", error);
        });
    },
    getConferenceName(conferenceId) {
      const conference = this.conferences[conferenceId];
      return conference ? conference.name : "Unknown";
    },
    getConferencePaperReviewDeadline(conferenceId) {
      const conference = this.conferences[conferenceId];
      return conference ? conference.paper_review_deadline : "Unknown";
    },
    async updateConference(publicationId, conferenceId) {
      if (!conferenceId) {
        alert("Please select a conference.");
        return;
      }
      try {
        await api.updatePublication(publicationId, { conferenceId });
        const publication = this.publications.find(
          (pub) => pub._id === publicationId
        );
        if (publication) {
          publication.conferenceId = conferenceId;
        }
        alert("Conference updated successfully!");
      } catch (error) {
        console.error("Error updating conference:", error);
        alert(
          "An error occurred while updating the conference. Please try again."
        );
      }
    },
    async assignReviewer(publication) {
      if (!publication.reviewerId) {
        alert("Please select a reviewer.");
        return;
      }
      try {
        await api.updatePublication(publication._id, {
          reviewerId: publication.reviewerId,
        });
        alert("Reviewer updated successfully!");
      } catch (error) {
        console.error("Error assigning reviewer:", error);
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
      this.newPublication.selectedFile = event.target.files[0];
    },
    async uploadPublication() {
      if (!this.newPublication.conferenceId) {
        this.uploadError = "Please select a valid conference.";
        return;
      }

      const formData = new FormData();
      formData.append("title", this.newPublication.title);
      formData.append("authorId", this.user_id);
      formData.append("co_authors", this.newPublication.co_authors);
      formData.append("key_words", this.newPublication.key_words);
      formData.append("conferenceId", this.newPublication.conferenceId);
      formData.append("file", this.newPublication.selectedFile);

      try {
        await api.uploadPublication(formData);
        alert("Publication uploaded successfully!");
        this.newPublication = {
          title: "",
          authorId: "",
          selectedFile: null,
          co_authors: "",
          key_words: "",
          conferenceId: "",
        };
        this.uploadError = null;
        // Reset file input
        this.$refs.fileInput.value = "";
        this.fetchPublications();
      } catch (error) {
        this.uploadError = error.response?.data?.error || "Upload failed";
      }
    },
    async downloadPublication(fileId, filename) {
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
    async downloadPublications(type) {
      try {
        let publicationsToDownload = [];
        let zipFileName = "";

        if (type === 'selected') {
          if (this.selectedPublications.length === 0) {
            alert("Please select publications to download.");
            return;
          }
          publicationsToDownload = this.publications.filter(pub =>
              this.selectedPublications.includes(pub._id)
          );
          zipFileName = "selected_publications.zip";
        } else if (type === 'filtered') {
          const filteredPublications = this.filteredAllPublications;
          if (filteredPublications.length === 0) {
            alert("No publications available to download.");
            return;
          }
          publicationsToDownload = filteredPublications;
          zipFileName = "filtered_publications.zip";
        }

        const zip = new JSZip();
        let count = 0;

        for (const publication of publicationsToDownload) {
          if (publication.fileId) {
            const response = await api.downloadPublication(publication.fileId);
            const blob = new Blob([response.data], {
              type: response.headers["content-type"],
            });
            const filename = `${publication.title}.pdf`;

            zip.file(filename, blob);
            count++;
          }
        }

        if (count > 0) {
          zip.generateAsync({ type: "blob" }).then((content) => {
            const link = document.createElement("a");
            link.href = URL.createObjectURL(content);
            link.download = zipFileName;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(link.href);
          });
        } else {
          alert("No files available for download.");
        }
      } catch (error) {
        console.error("Error downloading publications:", error.message);
        alert("An error occurred while downloading the publications.");
      }
    },
    isBeforeDeadline(conferenceId) {
      if (!conferenceId || !this.conferences[conferenceId]) {
        return false;
      }

      const conferenceEndDate = new Date(
        this.conferences[conferenceId].end_date
      );
      return new Date() <= conferenceEndDate;
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
  text-align: center;
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

button:disabled {
  background-color: #ccc;
  color: #666;
  cursor: not-allowed;
}

form {
  margin-top: 20px;
}

input[type="text"],
select {
  display: block;
  margin-bottom: 10px;
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

.custom-checkbox {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 30px;
  height: 30px;
  border-radius: 5px;
  border: 2px solid #51948c;
  background-color: #fff;
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
}

.custom-checkbox:checked {
  background-color: #579f97;
  border-color:  #51948c;
}

.custom-checkbox:checked::before {
  content: 'X';
  position: absolute;
  top: 3px;
  left: 7px;
  font-size: 18px;
  color: white;
}

.custom-checkbox:hover {
  background-color:#add2cd;
  border-color: #51948c;
}

input[type="file"] {
  display: block;
  margin-bottom: 10px;
}

button[type="submit"] {
  padding: 10px 20px;
}

#downloadSelectedPublicationsBtn {
  margin-bottom: 20px;
  float: right;
}

.error-message {
  color: red;
  margin-top: 20px;
}

select {
  margin-right: 0px;
  padding: 8px;
}

.assign-reviewer-button {
  padding: 10px 20px;
  background-color: #579f97;
}

.assign-reviewer-button:hover,
.download-button:hover {
  background-color: #26e7aa;
}

.download-button {
  background-color: #579f97;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-overflow: ellipsis;
  /* Adds an ellipsis (...) when content overflows */
  white-space: nowrap;
  /* Prevents wrapping of content */
}

th {
  background-color: #f2f2f2;
}
</style>
