<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="logo">
        <img
            src="https://static.vecteezy.com/system/resources/previews/001/201/180/original/brain-png.png"
            alt="Logo"
            class="logo-img"
        />
        <span class="logo-text">PDFSubmit</span>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/about" class="nav-link">About</router-link>
        <router-link to="/login" class="nav-link" v-if="!isLoggedIn">Login</router-link>
        <router-link to="/sign-up" class="nav-link" v-if="!isLoggedIn">Sign Up</router-link>
        <router-link to="/publications" class="nav-link" v-if="isLoggedIn">Publications</router-link>
        <router-link to="/admin" class="nav-link" v-if="isAdmin && isLoggedIn">Manage Users</router-link>
        <button v-if="isLoggedIn" @click="logout" class="nav-link logout-btn">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script>
import { EventBus } from '../services/eventBus';
import api from '../services/api';
export default {
  data() {
    return {
      isLoggedIn: false,
      isAdmin: false,
      isParticipant: false,
      isReviewer: false,
    };
  },
  methods: {
    logout() {
      this.isLoggedIn = false;
      this.isAdmin = false;
      this.isParticipant = false;
      this.isReviewer = false;
      localStorage.removeItem('userToken');
      this.$router.push('/login');
      EventBus.emit('user-logged-out');
    },
    decodeTokenUpdateData(token) {
      api.decode_token({ token })
          .then(response => {
            const decodedToken = response.data.user;
            this.isAdmin = decodedToken.isAdmin;
            this.isParticipant = decodedToken.isParticipant;
            this.isReviewer = decodedToken.isReviewer;
            console.error(this.isAdmin);
          })
          .catch(error => {
            console.error("Token decoding failed", error.response ? error.response.data : error.message);
            alert("Token decoding failed: " + (error.response ? error.response.data : error.message));
          });
    },
  },
  mounted() {
    const userToken = localStorage.getItem('userToken');
    if (userToken && this.isLoggedIn) this.decodeTokenUpdateData(userToken)

    EventBus.on('user-logged-in', () => {
      const userToken = localStorage.getItem('userToken');
      if (userToken) {
        this.decodeTokenUpdateData(userToken)
        this.isLoggedIn = true;
      }
    });

    EventBus.on('user-logged-out', () => {
      this.isLoggedIn = false;
      this.isAdmin = false;
      this.isParticipant = false;
      this.isReviewer = false;
    });
  },
};
</script>

<style scoped>
.navbar {
  background-color: #734ae8;
  padding: 10px 20px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  display: flex;
  align-items: center;
}

.logo-img {
  width: 30px;
  height: 30px;
  margin-right: 10px;
}

.logo-text {
  color: white;
  font-size: 24px;
  font-weight: bold;
}

.nav-links {
  display: flex;
  align-items: center;
}

.nav-link {
  color: white;
  text-decoration: none;
  margin-left: 20px;
  font-size: 16px;
  font-weight: 600;
}

.nav-link:hover {
  color: #89d4cf;
}

.logout-btn {
  background-color: transparent;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
}

.logout-btn:hover {
  color: #f44336;
}

@media screen and (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    align-items: flex-start;
  }
  .nav-links {
    flex-direction: column;
  }
  .nav-link {
    margin-left: 0;
    margin-bottom: 10px;
  }
}
</style>