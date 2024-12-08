<template>
    <div class="student-publications">
      <h1>Your Publications</h1>
      
      <!-- Displaying a list of publications -->
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Authors</th>
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
            <td>{{ publication.status }}</td>
            <td>
              <!-- Edit and Delete options -->
              <button v-if="publication.status === 'drafted'" @click="editPublication(publication)">Edit</button>
              <button v-if="publication.status === 'drafted'" @click="deletePublication(publication.id)">Delete</button>
              <button v-if="publication.status !== 'submitted'" @click="submitPublication(publication)">Submit</button>
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
  
      <div v-if="uploadError" class="error-message">
        <p>{{ uploadError }}</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        publications: [
          { id: 1, title: 'Publication 1', authors: ['Student 1'], status: 'drafted', fileUrl: 'path/to/publication1.pdf' },
          { id: 2, title: 'Publication 2', authors: ['Student 2'], status: 'submitted', fileUrl: 'path/to/publication2.pdf' },
          // Add more dummy publications as needed
        ],
        newPublication: {
          title: '',
          authors: '',
          file: null,
        },
        uploadError: null,
      };
    },
    methods: {
      // Submit publication logic
      submitPublication(publication) {
        if (this.isBeforeDeadline()) {
          publication.status = 'submitted'; // Update the status to 'submitted'
          console.log(`Publication ${publication.title} submitted.`);
        } else {
          alert('Deadline has passed. You cannot submit the publication.');
        }
      },
  
      // Edit publication logic
      editPublication(publication) {
        console.log(`Editing publication ${publication.title}`);
        // Implement editing logic, such as opening a modal or redirecting to an edit page
      },
  
      // Delete publication logic
      deletePublication(publicationId) {
        console.log(`Deleting publication with ID: ${publicationId}`);
        this.publications = this.publications.filter(pub => pub.id !== publicationId);
      },
  
      // Handle file upload
      handleFileUpload(event) {
        this.newPublication.file = event.target.files[0];
      },
  
      // Upload publication logic
      uploadPublication() {
        if (!this.newPublication.file) {
          this.uploadError = 'Please select a file to upload.';
          return;
        }
  
        // Simulate a successful upload and add the new publication to the list
        const newPub = {
          ...this.newPublication,
          id: this.publications.length + 1,
          status: 'drafted',
          fileUrl: URL.createObjectURL(this.newPublication.file), // Generate temporary file URL
        };
  
        this.publications.push(newPub);
        this.newPublication = { title: '', authors: '', file: null }; // Reset the form
        this.uploadError = null; // Reset error message
      },
  
      // Download publication logic
      downloadPublication(fileUrl) {
        const link = document.createElement('a');
        link.href = fileUrl;
        link.download = fileUrl.split('/').pop();
        link.click();
      },
  
      // Helper method to check if it's before the deadline
      isBeforeDeadline() {
        const deadline = new Date('2024-12-31'); // Example deadline, change as needed
        const currentDate = new Date();
        return currentDate <= deadline;
      },
    },
  };
  </script>
  
  <style scoped>
  .student-publications {
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
  
  .error-message {
    color: red;
    margin-top: 20px;
  }
  </style>
  