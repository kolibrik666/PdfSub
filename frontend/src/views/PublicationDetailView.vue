<template>
  <div class="publication-detail">
    <h1>{{ publication.title }}</h1>
    <p><strong>Authors:</strong> {{ publication.authors.join(', ') }}</p>
    <p><strong>Reviewer:</strong> {{ publication.reviewer }}</p>
    <p><strong>Abstract:</strong> {{ publication.abstract }}</p>
    <p><strong>Status:</strong> {{ publication.status }}</p>
    <button @click="goBack">Back to Publications</button>
    <button @click="downloadPublication(publication.fileUrl)">Download</button>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      publication: {},
    };
  },
  created() {
    const publicationId = this.$route.params.id;
    this.fetchPublication(publicationId);
  },
  methods: {
    fetchPublication(id) {
      api.getPublication(id).then(response => {
        this.publication = response.data;
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