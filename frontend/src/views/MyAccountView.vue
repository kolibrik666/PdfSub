<template>
    <div class="my-account-container">
        <!-- Form for editing user details -->
        <form @submit.prevent="updateAccount" class="account-form">
            <div class="form-group">
                <label for="name">Name:</label>
                <input type="text" placeholder="Enter your name" v-model="this.name" />
            </div>

            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" v-model="this.email" autocomplete="email" placeholder="Enter your email" />
            </div>
            <div class="form-group">
                <label for="password">New Password:</label>
                <input type="password" v-model="this.newPassword" autocomplete="new-password" placeholder="Enter new password" />
            </div>

            <div class="form-group">
                <label for="confirmPassword">Confirm Password:</label>
                <input type="password" v-model="this.confirmPassword"  autocomplete="new-password" placeholder="Confirm new password" />
            </div>

            <button type="submit" @click="updateUser()">Update</button>
        </form>
    </div>
</template>

<script>
import { decodeTokenUpdateData } from "../services/tokenUtils";
import api from "../services/api";

export default {
    data() {
        return {            
            user_id: "",
            name: "",
            email: "",
            newPassword: "",  
            confirmPassword: "",
            isLoggedIn: false,
            isAdmin: false,
            isParticipant: false,
            isReviewer: false
        };
    },
    methods: {
        setUserRole() {
            const token = localStorage.getItem("userToken");
            if (token) {
                decodeTokenUpdateData(token, this);
                this.isLoggedIn = true;
            }
        },
        async fetchUser(userId) {
            try {
                const response = await api.getUserById(userId);
                if (response.data) {
                    this.name = response.data['name'];
                    this.email = response.data['email'];
                    console.log("User fetched successfully:", response.data);
                }
            } catch (error) {
                console.error("Failed to fetch user:", error);
                alert("Failed to load user details");
            }
        },
        async updateUser() {
            console.log("Updating user...");

            if (this.newPassword && this.newPassword !== this.confirmPassword) {
                alert("Passwords do not match.");
                return;
            }

            const userUpdateData = {
                name: this.name,
                email: this.email
            };

            if (this.newPassword) {
                userUpdateData.password = this.newPassword;
            }

            try {
                await api.updateUser(this.user_id, userUpdateData);
                alert('User updated successfully');
            } catch (error) {
                console.error('Update failed', error);
                alert('Update failed');
            }
        },
    },
    watch: {
        user_id(newId) {
            if (newId) {
                this.fetchUser(newId);
            }
        },
    },
    created() {
        this.setUserRole();
    },
};
</script>
<style scoped>
.my-account-container {
    padding: 20px;
    margin-top: 150px;
}

.account-form {
    display: flex;
    flex-direction: column;
    gap: 15px;
    max-width: 400px;
    margin: 0 auto;
}

.form-group {
    display: flex;
    flex-direction: column;
}

input {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    padding: 10px 15px;
    background-color: #26e7aa;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    color: white;
}

button:hover {
    background-color: #1ac089;
}
</style>
