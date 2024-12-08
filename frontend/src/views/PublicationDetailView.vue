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
export default {
  data() {
    return {
      publication: {},
    };
  },
  created() {
    const publicationId = this.$route.params.id;
    // Fetch the publication details based on the ID
    // Replace with actual API call
    const publications = [
      { id: 1, title: 'Publication 1', authors: ['Author 1', 'Author 2'], reviewer: 'Reviewer 1', abstract: 'Abstract 1', status: 'drafted', fileUrl: 'path/to/publication1.pdf' },
      { id: 2, title: 'Publication 2', authors: ['Author 3'], reviewer: 'Reviewer 2', abstract: 'Abstract 2', status: 'submitted', fileUrl: 'path/to/publication2.docx' },
    ];
    this.publication = publications.find(pub => pub.id === parseInt(publicationId));
  },
  methods: {
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