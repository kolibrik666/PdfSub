<template>
  <div class="publication-detail" v-if="publication">
    <h1>{{ publication.title }}</h1>
    <p><strong>Author:</strong> {{ /*authors.join(', ') */author }}</p>
    <p><strong>Reviewer:</strong> {{ reviewer ? reviewer : 'No assigned reviewer' }}</p>
    <p><strong>Abstract:</strong> {{ publication.abstract }}</p>
    <p><strong>Status:</strong> {{ publication.review_status }}</p>
    <router-link to="/publications" class="button-link">Back to Publications</router-link>
    <button @click="downloadPublication(publication.fileUrl)">Download</button>
  </div>
  <div v-else>
    <p>Loading publication details...</p>
  </div>
</template>

<script>
import api from '../services/api';
export default {
  data() {
    return {
      publication: null,
      author: null,
      reviewer: null,
    };
  },
  created() {
    const publicationId = this.$route.params.id;
    this.fetchPublication(publicationId);
  },
  methods: {
    fetchPublication(id) {
      api.getPublication(id)
          .then(response => {
            this.publication = response.data;
            if (this.publication.author) {
              this.fetchAuthor(this.publication.authorId);
            } else {
              console.error("Author ID is undefined");
            }
            if (this.publication.reviewer) {
              this.fetchReviewer(this.publication.reviewer);
            }
          })
          .catch(error => {
            console.error("Failed to fetch publication", error);
            this.publication = {
              title: "Unknown",
              author: "Noone",
              abstract: "No abstract available",
              reviewer: "Unknown",
              rating: "FX",
              review_status: "Unknown",
              fileUrl: "#"
            };
          });
    },
    fetchAuthor(authorId) {
      if (!authorId) {
        console.error("Author ID is undefined");
        this.author = "Unknown";
        return;
      }
      api.getUserById(authorId)
          .then(response => {
            this.author = response.data.name;
          })
          .catch(error => {
            console.error("Failed to fetch author", error);
            this.author = "Unknown";
          });
    },
    fetchReviewer(reviewerId) {
      api.getUserById(reviewerId)
          .then(response => {
            this.reviewer = response.data.name;
          })
          .catch(error => {
            console.error("Failed to fetch reviewer", error);
            this.reviewer = null;
          });
    },
    downloadPublication(fileUrl) {
      const link = document.createElement('a');
      link.href = fileUrl;
      link.download = fileUrl.split('/').pop();
      link.click();
    },
  },
};
</script>

<style scoped>
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

.button-link:hover, button:hover {
  background-color: #5a3bb5;
}
</style>