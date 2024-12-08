<template>
  <div class="admin-view">
    <h1>Admin Panel</h1>
    <table>
      <thead>
        <tr>
          <th>Surname</th>
          <th>Name</th>
          <th>Email</th>
          <th>Password</th>
          <th>Role</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users" :key="user.email">
          <td><input type="text" v-model="user.surname" /></td>
          <td><input type="text" v-model="user.name" /></td>
          <td><input type="email" v-model="user.email" /></td>
          <td><input type="password" v-model="user.password" /></td>
          <td>
            <select v-model="user.role">
              <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
            </select>
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
      roles: ['Participant', 'Admin', 'Reviewer'],
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    fetchUsers() {
      api.getUsers().then(response => {
        this.users = response.data;
      });
    },
    updateUser(user) {
      console.log('Updating user:', user);
      // Implement update logic here
    },
    deleteUser(email) {
      console.log('Deleting user with email:', email);
      this.users = this.users.filter(user => user.email !== email);
    },
  },
};
</script>

<style scoped>
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