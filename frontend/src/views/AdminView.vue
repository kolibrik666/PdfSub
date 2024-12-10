<template>
  <div class="admin-container">
    <h1>Manage Users</h1>
    <table>
      <thead>
      <tr>
        <th>Email</th>
        <th>Name</th>
        <th>Surname</th>
        <th>Roles</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="user in users" :key="user.email">
        <td>{{ user.email }}</td>
        <td><input v-model="user.name" /></td>
        <td><input v-model="user.surname" /></td>
        <td>
          <label><input type="checkbox" v-model="user.isAdmin" /> Admin</label>
          <label><input type="checkbox" v-model="user.isStudent" /> Student</label>
          <label><input type="checkbox" v-model="user.isParticipant" /> Participant</label>
          <label><input type="checkbox" v-model="user.isReviewer" /> Reviewer</label>
        </td>
        <td>
          <button @click="updateUser(user)">Update</button>
          <button @click="deleteUser(user.email)">Delete</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      users: [],
    };
  },
  methods: {
    fetchUsers() {
      api.getUsers().then(response => {
        this.users = response.data;
      });
    },
    updateUser(user) {
      api.updateUser(user.email, {
        name: user.name,
        surname: user.surname,
        isAdmin: user.isAdmin,
        isStudent: user.isStudent,
        isParticipant: user.isParticipant,
        isReviewer: user.isReviewer,
      }).then(() => {
        alert('User updated successfully');
      }).catch(error => {
        console.error('Update failed', error);
        alert('Update failed');
      });
    },
    deleteUser(email) {
      api.deleteUser(email).then(() => {
        this.users = this.users.filter(user => user.email !== email);
        alert('User deleted successfully');
      }).catch(error => {
        console.error('Delete failed', error);
        alert('Delete failed');
      });
    },
  },
  mounted() {
    this.fetchUsers();
  },
};
</script>

<style scoped>
@import "~vue-multiselect/dist/vue-multiselect.min.css";

.admin-container {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  padding: 10px;
  border: 1px solid #ddd;
}

button {
  margin-right: 5px;
}

.admin-view {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #f2f2f2;
  color: #333;
}

td input[type="text"],
td input[type="email"],
td input[type="password"],
td select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  margin: 5px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

button + button {
  background-color: #f44336;
}

button + button:hover {
  background-color: #e53935;
}
</style>