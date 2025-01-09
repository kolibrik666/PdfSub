<template>
  <div class="publication-detail" v-if="publication">
    <h1 class="green-text">{{ publication.title }}</h1>
    <p><strong class="green-text">Author:</strong> {{ author }}</p>
    <p><strong class="green-text">Co-Authors:</strong> {{ co_authors }}</p>
    <p><strong class="green-text">Reviewer:</strong> {{ reviewer ? reviewer : 'No assigned reviewer' }}</p>
    <p><strong class="green-text">Status:</strong> {{ publication.review_status }}</p>

    <p v-if="!this.publication?.review_data"><strong class="green-text">Review: </strong>Not reviewed yet</p>
    <router-link to="/publications" class="button-link">Back to Publications</router-link>
    <button  class="download-button" @click="downloadPublication(publication.fileId, publication.title + '.pdf')"><i class="fa-solid fa-file-arrow-down"></i> Download</button>
    <button v-if="this.publication?.review_data" @click="toggleReviewDetails" class="fold-button">
      {{ reviewDetailsVisible ? 'Hide Review Details' : 'Show Review Details' }}
    </button>

    <!-- Review Data -->
    <div class="review-data">
      <div v-if="reviewDetailsVisible">
        <table class="review-table">
          <thead>
          <tr>
            <th>Criteria</th>
            <th>Rating/Comment</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="(value, criteria) in orderedReviewData" :key="criteria">
            <td><strong>{{ criteria }}</strong></td>
            <td>{{ value }}</td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Comments Section -->
    <div class="comments-section" >
      <h2>Comments</h2>
      <ul v-if="commentsWithNames.length">
        <li v-for="(comment, index) in commentsWithNames" :key="index">
          <p><strong class="green-text">{{ comment.reviewerName }}:</strong> {{ comment.comments }}</p>
          <small>{{ formatDate(comment.submittedAt) }}</small>
        </li>
      </ul>
      <p v-else>No comments yet. Be the first to comment!</p>

      <!-- Comment Form -->
      <h3>Add a Comment</h3>
      <form @submit.prevent="submitComment">
        <textarea
            v-model="newComment.comments"
            placeholder="Write your comment..."
            class="input-field"
        ></textarea>
        <button type="submit" >Submit Comment</button>
      </form>
    </div>
  </div>
  <div v-else>
    <p>Loading publication details...</p>
  </div>
</template>

<script>
import api from "../services/api";
import { decodeTokenUpdateData } from '../services/tokenUtils';

export default {
  data() {
    return {
      user_id: null,
      publication: null,
      author: null,
      co_authors: null,
      reviewerId: null,
      reviewer: null,
      isAuthorized: false,
      review_status: null,
      feedback: [],
      commentsWithNames: [],
      newComment: {
        reviewerId: "",
        comments: "",
      },
      reviewDetailsVisible: false,
    };
  },
  computed: {
    orderedReviewData() {
      if (!this.publication?.review_data) return {};

      const reviewData = this.publication.review_data;

      // Return the fields in the specific order
      return {
        "Aktuálnosť a náročnosť práce": reviewData["Aktuálnosť a náročnosť práce"],
        "Rozsah a úroveň dosiahnutých výsledkov": reviewData["Rozsah a úroveň dosiahnutých výsledkov"],
        "Analýza a interpretácia výsledkov a formulácia záveru práce": reviewData["Analýza a interpretácia výsledkov a formulácia záveru práce"],
        "Prehľadnosť a logická štruktúra práce": reviewData["Prehľadnosť a logická štruktúra práce"],
        "Formálna, jazyková a štylistická úprava práce": reviewData["Formálna, jazyková a štylistická úprava práce"],
        "Chýba názov práce v slovenskom alebo anglickom jazyku": reviewData["Chýba názov práce v slovenskom alebo anglickom jazyku"],
        "Chýba meno autora alebo školiteľa": reviewData["Chýba meno autora alebo školiteľa"],
        "Chýba pracovná emailová adresa autora alebo školiteľa": reviewData["Chýba pracovná emailová adresa autora alebo školiteľa"],
        "Chýba abstrakt v slovenskom alebo anglickom jazyku": reviewData["Chýba abstrakt v slovenskom alebo anglickom jazyku"],
        "Silné stránky práce": reviewData["Silné stránky práce"],
        "Slabé stránky práce": reviewData["Slabé stránky práce"]
      };
    },
  },
  created() {
    const publicationId = this.$route.params.id;
    this.fetchPublication(publicationId);
    const token = localStorage.getItem('userToken');
    if (token) {
      decodeTokenUpdateData(token, this);
      this.isLoggedIn = true;
    }
  },
  methods: {
    fetchPublication(id) {
      api.getPublication(id)
          .then((response) => {
            this.publication = response.data;
            this.feedback = response.data.feedback || [];
            this.commentsWithNames = [];
            this.review_status = response.data.review_status;

            if (this.publication.authorId) this.fetchUserName(this.publication.authorId, 'author');
            if (this.publication.co_authors) this.co_authors = this.publication.co_authors;
            if (this.publication.reviewerId) this.fetchUserName(this.publication.reviewerId, 'reviewer');

            Promise.all(this.feedback.map(async (comment) => {
              const reviewerName = await this.fetchUserNameId(comment.reviewerId);
              this.commentsWithNames.push({
                ...comment,
                reviewerName,
              });
            })).then(() => {
              this.commentsWithNames.sort((a, b) => new Date(b.submittedAt) - new Date(a.submittedAt)); // od najnovšieho
            });

            this.isAuthorized = this.user_id === this.publication.authorId || this.user_id === this.publication.reviewerId;
          })
          .catch((error) => {
            console.error("Failed to fetch publication", error);
          });
    },
    fetchUserName(userId, property) {
      api.getUserById(userId)
          .then((response) => {
            this[property] = response.data.name;
          })
          .catch(() => {
            this[property] = "Unknown";
          });
    },
    async fetchUserNameId(userId) {
      try {
        const response = await api.getUserById(userId);
        return response.data.name || "Unknown";
      } catch (error) {
        return "Unknown";
      }
    },
    submitComment() {
      if (!this.newComment.comments) {
        alert("Comment is required!");
        return;
      }
      const publicationId = this.$route.params.id;
      const commentData = {
        reviewerId: this.user_id, // Use saved user ID
        comments: this.newComment.comments,
      };

      api.addCommentToPublication(publicationId, commentData)
          .then((response) => {
            const newFeedback = response.data.feedback;
            this.feedback.push({
              ...newFeedback,
              reviewerName: "You", // Placeholder until fetched
            });

            // Reset form
            this.newComment.comments = "";
            this.fetchPublication(publicationId);
          })
          .catch((error) => {
            console.error("Failed to add comment", error);
          });
    },
    formatDate(date) {
      return new Date(date).toLocaleString();
    },
    async downloadPublication(fileId, filename) {
      try {
        const response = await api.downloadPublication(fileId);
        const blob = new Blob([response.data], { type: response.headers['content-type'] });
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
    toggleReviewDetails() {
      this.reviewDetailsVisible = !this.reviewDetailsVisible;
    },
  },
};
</script>

<style scoped>

review-data {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.review-data h2 {
  margin: 0;
}

.comments-section {
  margin-top: 30px;
}

.input-field {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  font-size: 14px;
}

.publication-detail {
  padding: 20px;
}

button, .button-link {
  margin-top: 20px;
  margin-right: 10px;
  padding: 10px 20px;
  background-color: #001e2bc5;
  border-radius: 5px;
  color: white;
  border: none;
  cursor: pointer;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  font-size: 16px;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  margin-bottom: 15px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 10px;
}

.button-link:hover, button:hover, .download-button:hover {
  background-color: #26e7aa;
}

.download-button {
  background-color: #579f97;
}

.review-table {
  margin-top: 20px;
}

</style>
