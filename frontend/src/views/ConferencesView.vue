<template>
  <div class="conferences-container">
    <h1>Conferences Management</h1>

    <!-- Form to Add a Conference -->
    <form @submit.prevent="addConference" class="conference-form">
      <div class="form-group">
        <label for="name">Conference Name:</label>
        <input v-model="newConference.name" id="name" required />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea v-model="newConference.description" id="description" required></textarea>
      </div>
      <div class="form-group">
        <label for="start_date">Start Date:</label>
        <input type="date" v-model="newConference.start_date" id="start_date" required />
      </div>
      <div class="form-group">
        <label for="end_date">End Date:</label>
        <input type="date" v-model="newConference.end_date" id="end_date" required />
      </div>
      <button type="submit" class="btn">Create Conference</button>
      <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
    </form>

    <!-- Table to Display Conferences -->
    <table class="conference-table">
      <thead>
      <tr>
        <th>Name</th>
        <th>Start Date</th>
        <th>End Date</th>
        <th>Description</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="conference in conferences" :key="conference._id">
        <td><input v-model="conference.name" /></td>
        <td><input type="date" v-model="conference.start_date" /></td>
        <td><input type="date" v-model="conference.end_date" /></td>
        <td><textarea v-model="conference.description"></textarea></td>
        <td>
          <button @click="updateConference(conference)" class="btn"><i class="fa-solid fa-pen-to-square"></i> Edit</button>
          <button @click="deleteConference(conference._id)" class="btn btn-danger"><i class="fa-regular fa-trash-can"></i> Delete</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  data() {
    return {
      conferences: [],
      newConference: {
        name: "",
        description: "",
        start_date: "",
        end_date: "",
      },
      errorMessage: null,
    };
  },
  methods: {
    fetchConferences() {
      api.getConferences()
          .then((response) => {
            this.conferences = response.data;
          })
          .catch((error) => {
            console.error("Error fetching conferences:", error);
          });
    },
    addConference() {
      api.createConference(this.newConference)
          .then(() => {
            alert("Conference created successfully!");
            this.fetchConferences();
            this.newConference = { name: "", description: "", start_date: "", end_date: "" };
            this.errorMessage = null;
          })
          .catch((error) => {
            console.error("Error creating conference:", error);
            this.errorMessage = error.response?.data?.error || "Failed to create conference.";
          });
    },
    updateConference(conference) {
      api.updateConference(conference._id, {
        name: conference.name,
        description: conference.description,
        start_date: conference.start_date,
        end_date: conference.end_date,
      })
          .then(() => {
            alert("Conference updated successfully");
            this.errorMessage = null; // Reset error message on successful update
          })
          .catch((error) => {
            console.error("Update failed", error);
            this.errorMessage = error.response?.data?.error || "Update failed";
          });
    },
    deleteConference(id) {
      api.deleteConference(id)
          .then(() => {
            this.conferences = this.conferences.filter(conference => conference._id !== id);
            alert("Conference deleted successfully");
          })
          .catch((error) => {
            console.error("Delete failed", error);
            alert("Delete failed");
          });
    },
  },
  created() {
    this.fetchConferences();
  },
};
</script>

<style scoped>

.error-message {
  color: red;
  margin-top: 10px;
}

.conferences-container {
  padding: 20px;
  max-width: 1000px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.conference-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 5px;
}

.form-group input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.btn {
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  background-color: #579f97;
  color: white;
  cursor: pointer;
}

.btn:hover {
  background-color: #26e7aa;
}

.btn-danger {
  background-color: #001e2bc5;
}

.btn-danger:hover {
  background-color: #26e7aa;
}

.conference-table {
  width: 100%;
  border-collapse: collapse;
}

.conference-table textarea{
  width: 90%;
}

.conference-table th, .conference-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}

.conference-table th {
  background-color: #f4f4f4;
}
</style>