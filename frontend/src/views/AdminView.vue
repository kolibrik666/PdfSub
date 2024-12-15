<template>
  <div class="admin-container">
    <h1>Manage Users</h1>
    <div class="filter-container">
      <input
          v-model="searchQuery"
          class="search-input"
          placeholder="Search by email or name"
      />
      <select v-model="selectedRole" class="role-select">
        <option value="">All Roles</option>
        <option value="admin">Admin</option>
        <option value="participant">Participant</option>
        <option value="reviewer">Reviewer</option>
      </select>
    </div>
    <table>
      <thead>
      <tr>
        <th>Email</th>
        <th>Name</th>
        <th>Roles</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="user in filteredUsers" :key="user.email">
        <td>{{ user.email }}</td>
        <td><input v-model="user.name" /></td>
        <td>
          <label><input type="checkbox" v-model="user.roles.isAdmin" /> Admin</label>
          <label><input type="checkbox" v-model="user.roles.isParticipant" /> Participant</label>
          <label><input type="checkbox" v-model="user.roles.isReviewer" /> Reviewer</label>
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
      searchQuery: '',
      selectedRole: '',
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter(user => {
        const searchLower = this.searchQuery.toLowerCase();
        const matchesSearch = user.email.toLowerCase().includes(searchLower) ||
            user.name.toLowerCase().includes(searchLower)
        const matchesRole = !this.selectedRole ||
            (this.selectedRole === 'admin' && user.roles.isAdmin) ||
            (this.selectedRole === 'participant' && user.roles.isParticipant) ||
            (this.selectedRole === 'reviewer' && user.roles.isReviewer);
        return matchesSearch && matchesRole;
      });
    },
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
        roles: {
          isAdmin: user.roles.isAdmin,
          isParticipant: user.roles.isParticipant,
          isReviewer: user.roles.isReviewer,
        }
      }).then(() => {
        alert('User updated successfully');
      }).catch(error => {
        console.error('Update failed', error);
        alert('Update failed');
      });
    },
    deleteUser(email) {
      api.deleteUser(email)
          .then(() => {
            this.users = this.users.filter(user => user.email !== email);
            alert('User deleted successfully');
          })
          .catch(error => {
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
.admin-container {
  padding: 20px;
}

.filter-container {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input[type="text"], select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.filter-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  gap: 1rem; /* Optional: Add spacing between elements */
}

.search-input,
.role-select {
  flex: 1;
  max-width: 50%; /* Ensure they don't exceed half the width */
  box-sizing: border-box; /* Include padding/border in width calculation */
}

.search-input {
  padding: 0.5rem; /* Add some padding for aesthetics */
}

.role-select {
  padding: 0.4rem; /* Slightly smaller padding for a dropdown */
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
</style>