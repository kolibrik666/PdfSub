<!-- frontend/src/views/AdminView.vue -->
<template>
  <div class="admin-view">
    <h1>Admin Panel</h1>
    <table>
      <thead>
      <tr>
        <th>Username</th>
        <th>Email</th>
        <th>Role</th>
        <th>Permissions</th>
        <th>Actions</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="user in users" :key="user.id">
        <td>{{ user.username }}</td>
        <td>{{ user.email }}</td>
        <td>
          <select v-model="user.role">
            <option v-for="role in roles" :key="role" :value="role">{{ role }}</option>
          </select>
        </td>
        <td>
          <input type="text" v-model="user.permissions" placeholder="Enter permissions" />
        </td>
        <td>
          <button @click="updateUser(user)">Update</button>
          <button @click="deleteUser(user.id)">Delete</button>
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
      users: [
        { id: 1, username: 'user1', email: 'user1@example.com', role: 'User', permissions: 'read' },
        { id: 2, username: 'user2', email: 'user2@example.com', role: 'Admin', permissions: 'read,write' },
        // Add more dummy users as needed
      ],
      roles: ['User', 'Admin', 'Moderator'],
    };
  },
  methods: {
    updateUser(user) {
      console.log('Updating user:', user);
      // Implement update logic here
    },
    deleteUser(userId) {
      console.log('Deleting user with ID:', userId);
      this.users = this.users.filter(user => user.id !== userId);
    },
  },
};
</script>

<style scoped>
.admin-view {
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