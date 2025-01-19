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
    <form @submit.prevent="createUser" class="create-user-form">
      <div class="form-group">
        <label for="username">Username:</label>
        <input
          type="text"
          v-model="newUser.username"
          placeholder="Enter Name"
          required
        />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input
          type="email"
          v-model="newUser.email"
          placeholder="Enter Email"
          required
        />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input
          type="password"
          v-model="newUser.password"
          placeholder="Enter Password"
          required
        />
      </div>
      <button type="submit">Create User</button>
    </form>
    <table>
      <thead>
        <tr>
          <th>Email</th>
          <th>Name</th>
          <th>Roles</th>
          <th>Update</th>
          <th>Manage Access</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in filteredUsers" :key="user.email">
          <td>{{ user.email }}</td>
          <td><input v-model="user.name" /></td>
          <td>
            <label
              ><input type="checkbox" v-model="user.roles.isAdmin" />
              Admin</label
            >
            <label
              ><input type="checkbox" v-model="user.roles.isParticipant" />
              Participant</label
            >
            <label
              ><input type="checkbox" v-model="user.roles.isReviewer" />
              Reviewer</label
            >
          </td>
          <td>
            <button @click="updateUser(user)" class="update-button">
              Update User Details
            </button>
          </td>
          <td>
            <button
              @click="toggleUserAccess(user)"
              :class="{ enabled: user.isEnabled, disabled: !user.isEnabled }"
            >
              {{ user.isEnabled ? "Ban User" : "Permit User" }}
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import api from "../services/api";

export default {
  data() {
    return {
      users: [],
      searchQuery: "",
      selectedRole: "",
      newUser: {
        username: "",
        email: "",
        password: "",
      },
    };
  },
  computed: {
    filteredUsers() {
      return this.users.filter((user) => {
        const searchLower = this.searchQuery.toLowerCase();
        const matchesSearch =
          user.email.toLowerCase().includes(searchLower) ||
          user.name.toLowerCase().includes(searchLower);
        const matchesRole =
          !this.selectedRole ||
          (this.selectedRole === "admin" && user.roles.isAdmin) ||
          (this.selectedRole === "participant" && user.roles.isParticipant) ||
          (this.selectedRole === "reviewer" && user.roles.isReviewer);
        return matchesSearch && matchesRole;
      });
    },
  },
  methods: {
    fetchUsers() {
      api.getUsers().then((response) => {
        this.users = response.data;
      });
    },
    createUser() {
      api
        .register({
          email: this.newUser.email,
          password: this.newUser.password,
          name: this.newUser.username,
        })
        .then(() => {
          alert("User created successfully");
          this.newUser = { username: "", email: "", password: "" };
          this.fetchUsers();
        })
        .catch((error) => {
          console.error("Error creating user:", error);
          alert("Failed to create user.");
        });
    },
    updateUser(user) {
      api
        .updateUser(user.email, {
          name: user.name,
          roles: {
            isAdmin: user.roles.isAdmin,
            isParticipant: user.roles.isParticipant,
            isReviewer: user.roles.isReviewer,
          },
          isEnabled: user.isEnabled,
        })
        .then(() => {
          alert("User updated successfully");
        })
        .catch((error) => {
          console.error("Update failed", error);
          alert("Update failed");
        });
    },
    toggleUserAccess(user) {
      // Toggle the user's `isEnabled` status
      const updatedStatus = !user.isEnabled;

      // Send the update to the backend
      api
        .updateUser(user.email, {
          isEnabled: updatedStatus, // Update the isEnabled field
        })
        .then(() => {
          user.isEnabled = updatedStatus; // Update the local user object on success
          alert(
            `User access ${updatedStatus ? "enabled" : "disabled"} successfully`
          );
        })
        .catch((error) => {
          console.error("Failed to toggle access:", error);
          alert("Failed to update user access.");
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

input[type="text"],
select {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.create-user-form {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  align-items: center;
}

.create-user-form .form-group {
  display: flex;
  flex-direction: column;
}

.create-user-form input {
  padding: 5px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
  text-align: center;
}

th,
td {
  padding: 10px;
  border: 1px solid #ddd;
}

button:hover {
  background-color: #26e7aa;
}

.update-button {
  background-color: #579f97;
}
</style>
