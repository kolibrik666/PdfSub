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
          <router-link to="/login" class="nav-link">Login</router-link>
          <router-link to="/sign_up" class="nav-link">Sign Up</router-link>
          
          <!-- Conditionally render the Logout link if the user is logged in -->
          <button v-if="isLoggedIn" @click="logout" class="nav-link logout-btn">
            Logout
          </button>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    data() {
      return {
        // Assuming user authentication status is stored in a variable or Vuex store
        isLoggedIn: false, // Set this dynamically based on the user's login state
      };
    },
    methods: {
      logout() {
        // Logic to log the user out (e.g., clear localStorage or reset Vuex state)
        this.isLoggedIn = false;
        // Redirect to home or login page
        this.$router.push('/login');
      },
    },
    mounted() {
      // Check if the user is logged in (e.g., check token or session)
      // For now, let's assume localStorage holds a flag or token
      const userToken = localStorage.getItem('userToken');
      if (userToken) {
        this.isLoggedIn = true;
      }
    },
  };
  </script>
  
  <style scoped>
  /* Basic styling for the navigation bar */
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
  