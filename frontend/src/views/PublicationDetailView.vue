<template>
  <div class="publication-detail" v-if="publication">
    <h1>{{ publication.title }}</h1>
    <p><strong>Authors:</strong> {{ publication.authors.join(', ') }}</p>
    <p><strong>Reviewer:</strong> {{ publication.reviewer }}</p>
    <p><strong>Abstract:</strong> {{ publication.abstract }}</p>
    <p><strong>Status:</strong> {{ publication.status }}</p>
    <button @click="goBack">Back to Publications</button>
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
            if (!this.publication.authors) {
              this.publication.authors = [];
            }
          })
          .catch(error => {
            console.error("Failed to fetch publication", error);
            this.publication = {
              title: "Unknown",
              authors: [],
              reviewer: "Unknown",
              abstract: "No abstract available",
              status: "Unknown",
              fileUrl: "#"
            };
          });
    },
    goBack() {
      this.$router.push('/manage-publications');
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

button {
  margin-top: 20px;
  margin-right: 10px;
}
</style>