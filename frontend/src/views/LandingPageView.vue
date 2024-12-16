<template>
    <div>
      <!-- Banner Section -->
      <div class="banner">
        <img src="https://images.unsplash.com/photo-1535540674795-d2e704953bf1?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D" alt="Banner Image" class="banner-image" />
         <!-- https://images.unsplash.com/photo-1535540674795-d2e704953bf1?q=80&w=2071&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D -->
        <!--  <img src="../assets/img/lecture-seats.jpg" alt="Banner Image" class="banner-image" /> -->
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
.cta-button:hover {
  background-color: #0c01018b;
}

</style>