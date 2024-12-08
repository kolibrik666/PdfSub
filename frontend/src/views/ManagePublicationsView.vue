<!-- frontend/src/views/ManagePublicationsView.vue -->
<template>
  <div class="manage-publications">
    <h1>Manage Publications</h1>
    <table>
      <thead>
      <tr>
        <th>Title</th>
        <th>Author</th>
        <th>Reviewer</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="publication in publications" :key="publication.id">
        <td>{{ publication.title }}</td>
        <td>{{ publication.author }}</td>
        <td>
          <select v-model="publication.reviewer">
            <option v-for="reviewer in reviewers" :key="reviewer" :value="reviewer">{{ reviewer }}</option>
          </select>
        </td>
        <td>
          <button @click="assignReviewer(publication)">Assign Reviewer</button>
          <button @click="deletePublication(publication.id)">Delete</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      publications: [
        { id: 1, title: 'Publication 1', author: 'Author 1', reviewer: '' },
        { id: 2, title: 'Publication 2', author: 'Author 2', reviewer: '' },
        // Add more dummy publications as needed
      ],
      reviewers: ['Reviewer 1', 'Reviewer 2', 'Reviewer 3'],
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
</style>