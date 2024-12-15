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
      <h2>Feedback</h2>
      <ul v-if="feedback && feedback.length">
        <li v-for="(comment, index) in feedback" :key="index">
          <p><strong>{{ comment.reviewerName }}:</strong> {{ comment.comments }}</p>
          <small>{{ formatDate(comment.submittedAt) }}</small>
        </li>
      </ul>
      <p v-else>No comments yet. Be the first to comment!</p>

      <!-- Comment Form -->
      <h3>Add a Comment</h3>
      <form @submit.prevent="submitComment">
        <input
            v-model="newComment.reviewerId"
            type="text"
            placeholder="Your reviewer ID"
            class="input-field"
        />
        <textarea
            v-model="newComment.comments"
            placeholder="Write your comment..."
            class="input-field"
        ></textarea>
        <button type="submit">Submit Comment</button>
      </form>
    </div>
  </div>
  <div v-else>
    <p>Loading publication details...</p>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      publication: null,
      author: null,
      co_authors: null,
      reviewer: null,
      feedback: [],
      newComment: {
        reviewerId: "",
        comments: "",
      },
    };
  },
  created() {
    const publicationId = this.$route.params.id;
    this.fetchPublication(publicationId);
  },
  methods: {
    fetchPublication(id) {
      api.getPublication(id)
          .then((response) => {
            this.publication = response.data;
            this.feedback = response.data.feedback || [];

            this.feedback.forEach((comment, index) => {
              this.fetchReviewerName(comment.reviewerId, index);
            });
            if (this.publication.authorId) this.fetchUser(this.publication.authorId);
            if (this.publication.co_authors) this.co_authors = this.publication.co_authors;
            if (this.publication.reviewer) this.fetchUser(this.publication.reviewer);
          })
          .catch((error) => {
            console.error("Failed to fetch publication", error);
          });
    },
    fetchUser(authorId) {
      api.getUserById(authorId)
          .then((response) => {
            this.author = response.data.name 
          })
          .catch(() => {
            this.author = "Unknown";
          });
    },
    fetchReviewerName(reviewerId, index) {
      api.getUserById(reviewerId)
          .then((response) => {
            this.feedback[index].reviewerName =
                response.data.name 
          })
          .catch(() => {
            this.feedback[index].reviewerName = "Unknown Reviewer";
          });
    },
    submitComment() {
      if (!this.newComment.comments || !this.newComment.reviewerId) {
        alert("Both reviewer ID and comment are required!");
        return;
      }

      const publicationId = this.$route.params.id;

      api.addCommentToPublication(publicationId, this.newComment)
          .then((response) => {
            const newFeedback = response.data.feedback;
            this.feedback.push({
              ...newFeedback,
              reviewerName: "You", // Placeholder until fetched
            });

            // Reset form
            this.newComment.comments = "";
            this.newComment.reviewerId = "";
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
  background-color: #734ae8;
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
  background-color: #5a3bb5;
}
</style>