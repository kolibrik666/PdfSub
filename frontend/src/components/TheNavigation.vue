<template>
  <nav class="navbar">
    <div class="navbar-container">
      <div class="logo">
        <img
            src="logo-img.ico"
            alt="Logo"
            class="logo-img"
        />
        <span class="logo-text">PDFSubmit</span>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link" v-if="!isLoggedIn">Home</router-link>
        <router-link to="/login" class="nav-link" v-if="!isLoggedIn">Login</router-link>
        <router-link to="/sign-up" class="nav-link" v-if="!isLoggedIn">Sign Up</router-link>
        <router-link to="/publications" class="nav-link" v-if="isLoggedIn">Publications</router-link>
        <router-link to="/admin" class="nav-link" v-if="isAdmin && isLoggedIn">Manage Users</router-link>
        <router-link to="/conferences" class="nav-link" v-if="isAdmin && isLoggedIn">Manage Conferences</router-link>
        <router-link to="/my-account" class="nav-link" v-if="isLoggedIn">My Account</router-link>
        <button v-if="isLoggedIn" @click="logout" class="logout-button">Logout ({{ email }})</button>
      </div>
    </div>
  </nav>
</template>

<script>
import { EventBus } from '../services/eventBus';
import { decodeTokenUpdateData } from '../services/tokenUtils';

export default {
  data() {
    return {
      email: '', 
      isLoggedIn: false,
      isAdmin: false,
      isParticipant: false,
      isReviewer: false,
    };
  },
  methods: {
    logout() {
      this.email = '';
      this.isLoggedIn = false;
      this.isAdmin = false;
      this.isParticipant = false;
      this.isReviewer = false;
      localStorage.removeItem('userToken');
      this.$router.push('/login');
      EventBus.emit('user-logged-out');
    },
    decodeTokenData(token) {
      decodeTokenUpdateData(token, this);
    },
  },
  mounted() {
    const userToken = localStorage.getItem('userToken');
    if (userToken) {
      this.decodeTokenData(userToken);
      this.isLoggedIn = true;
    }
    EventBus.on('user-logged-in', () => {
      const userToken = localStorage.getItem('userToken');
      if (userToken) {
        this.decodeTokenData(userToken)
        this.isLoggedIn = true;
      }
    });

    EventBus.on('user-logged-out', () => {
      this.email = '';
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
  background-color: #579f97;
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
  color: #26e7aa;
}

.logout-button {
  all: unset; /* Resets all default button styles */
  background-color: transparent;
  display: inline-block;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  font-family: Poppins, sans-serif;
  margin: 0 0 0 40px;
  font-weight: 600;
}

.logout-button:hover {
  color: #26e7aa;
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