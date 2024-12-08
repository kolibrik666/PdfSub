<template>
  <div class="manage-publications">
    <h1>Manage Publications</h1>
    <table>
      <thead>
      <tr>
        <th>Title</th>
        <th>Authors</th>
        <th>Reviewer</th>
        <th>Status</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="publication in publications" :key="publication.id">
        <td>
          <router-link :to="{ name: 'publication-detail', params: { id: publication.id } }">
            {{ publication.title }}
          </router-link>
        </td>
        <td>{{ publication.authors.join(', ') }}</td>
        <td>
          <select v-model="publication.reviewer">
            <option v-for="reviewer in reviewers" :key="reviewer" :value="reviewer">{{ reviewer }}</option>
          </select>
        </td>
        <td>{{ publication.status }}</td>
        <td>
          <button @click="assignReviewer(publication)">Assign Reviewer</button>
          <button @click="deletePublication(publication.id)">Delete</button>
          <button @click="downloadPublication(publication.fileUrl)">Download</button>
        </td>
      </tr>
      </tbody>
    </table>
    <h2>Upload New Publication</h2>
    <form @submit.prevent="uploadPublication">
      <input type="text" v-model="newPublication.title" placeholder="Title" required />
      <input type="text" v-model="newPublication.authors" placeholder="Authors (comma separated)" required />
      <input type="file" @change="handleFileUpload" accept=".pdf,.docx" required />
      <button type="submit">Upload</button>
    </form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      publications: [
        { id: 1, title: 'Publication 1', authors: ['Author 1', 'Author 2'], reviewer: '', status: 'drafted', fileUrl: 'path/to/publication1.pdf' },
        { id: 2, title: 'Publication 2', authors: ['Author 3'], reviewer: '', status: 'submitted', fileUrl: 'path/to/publication2.docx' },
        // Add more dummy publications as needed
      ],
      reviewers: ['Reviewer 1', 'Reviewer 2', 'Reviewer 3'],
      newPublication: {
        title: '',
        authors: '',
        file: null,
      },
    };
  },
  methods: {
    assignReviewer(publication) {
      console.log('Assigning reviewer:', publication);
      // Implement assign reviewer logic here
    },
    deletePublication(publicationId) {
      console.log('Deleting publication with ID:', publicationId);
      this.publications = this.publications.filter(pub => pub.id !== publicationId);
    },
    handleFileUpload(event) {
      this.newPublication.file = event.target.files[0];
    },
    uploadPublication() {
      console.log('Uploading publication:', this.newPublication);
      // Implement upload logic here
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
.manage-publications {
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
</style>