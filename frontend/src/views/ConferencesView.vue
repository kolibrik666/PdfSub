<template>
  <div>
    <h1>Conferences Management</h1>

    <!-- Form to Add a Conference -->
    <form @submit.prevent="addConference">
      <div>
        <label for="name">Conference Name:</label>
        <input v-model="newConference.name" id="name" required />
      </div>
      <div>
        <label for="start_date">Start Date:</label>
        <input type="date" v-model="newConference.start_date" id="start_date" required />
      </div>
      <div>
        <label for="end_date">End Date:</label>
        <input type="date" v-model="newConference.end_date" id="end_date" required />
      </div>
      <button type="submit">Create Conference</button>
    </form>

    <!-- Table to Display Conferences -->
    <table>
      <thead>
      <tr>
        <th>Name</th>
        <th>Start Date</th>
        <th>End Date</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="conference in conferences" :key="conference._id">
        <td>{{ conference.name }}</td>
        <td>{{ conference.start_date }}</td>
        <td>{{ conference.end_date }}</td>
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
        start_date: "",
        end_date: "",
      },
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
            this.newConference = { name: "", start_date: "", end_date: "" };
          })
          .catch((error) => {
            console.error("Error creating conference:", error);
          });
    },
  },
  created() {
    this.fetchConferences();
  },
};
</script>

<style scoped>
form {
  margin-bottom: 20px;
}

form div {
  margin: 10px 0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border: 1px solid #ccc;
}

th {
  background-color: #f4f4f4;
}
</style>
