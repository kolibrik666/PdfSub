<template>
  <div class="publication-detail" v-if="publication">
    <h1>{{ publication.title }}</h1>
    <p><strong>Author:</strong> {{ author }}</p>
    <p><strong>Co-Authors:</strong> {{ co_authors }}</p>
    <p><strong>Reviewer:</strong> {{ reviewer ? reviewer : 'No assigned reviewer' }}</p>
    <p><strong>Status:</strong> {{ publication.review_status }}</p>
    <p><strong>Rating:</strong> {{ publication.rating }}</p>

    <router-link to="/publications" class="button-link">Back to Publications</router-link>
    <button @click="downloadPublication(publication.fileUrl)">Download</button>
    <!-- Comments Section -->
    <div class="comments-section">
      <h2>Comments</h2>
      <ul v-if="commentsWithNames.length">
        <li v-for="(comment, index) in commentsWithNames" :key="index">
          <p><strong>{{ comment.reviewerName }}:</strong> {{ comment.comments }}</p>
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
            :disabled="!isAuthorized"
        ></textarea>
        <button type="submit" :disabled="!isAuthorized">Submit Comment</button>
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
      feedback: [],
      commentsWithNames: [],
      newComment: {
        reviewerId: "",
        comments: "",
      },
    };
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
            this.commentsWithNames = []; // Reset the array

            if (this.publication.authorId) this.fetchUserName(this.publication.authorId, 'author');
            if (this.publication.co_authors) this.co_authors = this.publication.co_authors;
            if (this.publication.reviewerId) this.fetchUserName(this.publication.reviewerId, 'reviewer');

            Promise.all(this.feedback.map(async (comment) => {
              const reviewerName = await this.fetchUserNameId(comment.reviewerId);
              this.commentsWithNames.push({
                ...comment,
                reviewerName,
              });
            }));
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
        console.log(response.data); // See what data you're getting
        return response.data.name || "Unknown";
      } catch (error) {
        if (error.response) {
          console.error('Server error:', error.response);
        } else if (error.request) {
          console.error('No response received:', error.request);
        } else {
          console.error('Error', error.message);
        }
        return "Unknown";
      }
    },
    submitComment() {
      if (!this.newComment.comments) {
        alert("Comment is required!");
        return;
      }

      const publicationId = this.$route.params.id;

      if (!this.isAuthorized) {
        alert("You are not authorized to comment on this publication.");
        return;
      }

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
    downloadPublication(fileUrl) {
      const link = document.createElement("a");
      link.href = fileUrl;
      link.download = fileUrl.split("/").pop();
      link.click();
    },
  },
};
</script>

<style scoped>
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
  background-color: #000000;
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

.button-link:hover, button:hover {
  background-color: #26e7aa;
}
</style>