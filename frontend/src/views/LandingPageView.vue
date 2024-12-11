<template>
    <div>
      <!-- Banner Section -->
      <div class="banner">
        <img src="../assets/img/lecture-seats.jpg" alt="Banner Image" class="banner-image" />
        <div class="cta-buttons">
          <router-link to="/login">
            <button class="cta-button login-button">Login</button>
          </router-link>
          <router-link to="/sign-up">
            <button class="cta-button signup-button">Sign Up</button>
          </router-link>
        </div>
      </div>
  
      <!-- Landing Page Content -->
      <div class="landing-page">
        <!-- Informational Row -->
        <div class="info-row">
          <div class="info-box">
            <h3>Feature 1</h3>
            <p>This is the first feature of our app, which helps you do amazing things.</p>
          </div>
          <div class="info-box">
            <h3>Feature 2</h3>
            <p>Our second feature is designed to save you time and increase productivity.</p>
          </div>
          <div class="info-box">
            <h3>Feature 3</h3>
            <p>Explore our third feature to streamline your workflow with ease.</p>
          </div>
          <div class="info-box">
            <h3>Feature 4</h3>
            <p>With our fourth feature, you can automate your processes effortlessly.</p>
          </div>
        </div>
  
        <!-- FAQ Section -->
        <div class="faq">
          <h2>FAQ</h2>
          <div v-for="(item, index) in faqItems" :key="index" class="faq-item">
            <button class="faq-toggle" @click="toggleFaq(index)">
              <h3>{{ item.question }}</h3>
            </button>
            <div v-show="item.isOpen" class="faq-answer">
              <p>{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  
     
  
  <script>
  export default {
    name: 'LandingPage',
    data() {
      return {
        // FAQ items with toggle state
        faqItems: [
          { question: "What is this website about?", answer: "This website provides a simple landing page to demonstrate Vue.js capabilities.", isOpen: false },
          { question: "How can I get started?", answer: "Click the 'Sign Up' button to create an account and start using the app.", isOpen: false },
          { question: "Is there a mobile version?", answer: "Yes, this site is mobile-friendly and fully responsive.", isOpen: false },
        ]
      };
    },
    methods: {
      toggleFaq(index) {
        // Toggle the visibility of the answer
        this.faqItems[index].isOpen = !this.faqItems[index].isOpen;
      }
    }
  };
  </script>
  
  <style scoped>
  /* General Styling */
  body {
    font-family: Arial, sans-serif;
    margin: 0;
    padding: 0;
  }
  
  .landing-page {
    text-align: center;
    max-width: 1300px;
    margin: 0 auto;
  }
  
  /* Banner Styling */
  .banner {
  position: relative;
  width: 100%; /* Full width */
  height: 400px; /* Set the desired height for the banner */
  overflow: hidden; /* Ensures no overflow content from the image */
  
}

.banner-image {
  width: 100%; /* Full width */
  height: auto; /* Maintain aspect ratio */
  display: block; /* Removes extra spacing */
}
  
  .cta-buttons {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    display: flex;
    gap: 20px;
  }
  
  .cta-button {
    font-size: 16px;
    padding: 15px 30px;
    margin: 10px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    transition: background-color 0.3s;
  }
  
  .login-button {
    background-color: #4CAF50;
    color: white;
  }
  
  .signup-button {
    background-color: #2196F3;
    color: white;
  }
  
  .cta-button:hover {
    opacity: 0.8;
  }
  
  /* Informational Row */
  .info-row {
    display: flex;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 20px;
    margin-top: 40px;
  }
  
  .info-box {
    flex: 1;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .info-box h3 {
    font-size: 22px;
    margin-bottom: 15px;
  }
  
  .info-box p {
    font-size: 14px;
    color: #555;
  }
  
  /* FAQ Section */
  .faq {
    margin: 40px 0;
    text-align: left;
    max-width: 800px;
    margin: 40px auto;
  }
  
  .faq h2 {
    font-size: 24px;
    margin-bottom: 20px;
  }
  
  .faq-item {
    margin-bottom: 20px;
  }
  
  .faq-toggle {
    background-color: #f5f5f5;
    border: none;
    width: 100%;
    text-align: left;
    padding: 15px;
    font-size: 18px;
    cursor: pointer;
    border-radius: 5px;
    transition: background-color 0.3s;
  }
  
  .faq-toggle:hover {
    background-color: #e0e0e0;
  }
  
  .faq-answer {
    padding: 10px 20px;
    background-color: #f9f9f9;
    border-left: 4px solid #2196F3;
    margin-top: 10px;
  }
  </style>
  