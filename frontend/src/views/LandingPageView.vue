<template>
  <div>
    <!-- Banner Section -->
    <div class="banner">
      <img src="https://builder.bootstrapmade.com/static/img/hero-bg-2.jpg" alt="banner image" class="banner-image" />
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
      <div class="info-row">
        <div class="info-box">
          <div class="icon-circle"><i class="fas fa-user"></i></div>
          <h3>For Participants</h3>
          <p>Whether you're a student, researcher, or PhD candidate, the CMS equips you with the tools to submit and present your research successfully.</p>
        </div>
        <div class="info-box">
          <div class="icon-circle"><i class="fas fa-graduation-cap"></i></div>
          <h3>For Students</h3>
          <p>Easily submit papers, track review progress, and stay updated on deadlines. Monitor every stage, from submission to final evaluation, with notifications keeping you informed throughout.</p>
        </div>
        <div class="info-box">
          <div class="icon-circle"><i class="fas fa-clipboard-check"></i></div>
          <h3>For Reviewers</h3>
          <p>Access assigned papers, provide detailed feedback, and efficiently manage your review tasks.</p>
        </div>
        <div class="info-box">
          <div class="icon-circle"><i class="fas fa-cogs"></i></div>
          <h3>For Administrators</h3>
          <p>Manage conferences, oversee participants and reviewers, and generate comprehensive reports on submissions and reviews.</p>
        </div>
      </div>

      <!-- Current Conferences Section -->
      <h2>Current Conferences</h2>
      <div class="current-conferences" v-if="currentConferences.length > 0">
        <div class="conferences-row">
          <div class="conference-box" v-for="conference in currentConferences" :key="conference._id">
            <h3>{{ conference.name }}</h3>
            <p>{{ conference.description }}</p>
            <p><strong>Start Date:</strong> {{ conference.start_date }}</p>
            <p><strong>End Date:</strong> {{ conference.end_date }}</p>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No current conferences available at the moment.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  data() {
    return {
      conferences: [],
    };
  },
  mounted() {
    this.fetchConferences();
  },
  computed: {
    currentConferences() {
      const currentDate = new Date();
      return Object.values(this.conferences).filter(conference => {
        const startDate = new Date(conference.start_date);
        const endDate = new Date(conference.end_date);
        return currentDate >= startDate && currentDate <= endDate;
      });
    }
  },
  methods: {
    async fetchConferences() {
      try {
        const response = await api.getConferences();
        this.conferences = response.data.reduce((acc, conf) => {
          acc[conf._id] = conf;
          return acc;
        }, {});
      } catch (error) {
        console.error("Error fetching conferences:", error);
      }
    },
  }
};
</script>

<style scoped>
.current-conferences {
  padding: 40px 20px;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  flex-direction: column;
}

.conferences-row {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 20px;
  width: 100%;
}

.conference-box {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  flex: 1;
  max-width: 300px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.conference-box h3 {
  font-size: 18px;
  margin-bottom: 10px;
}

.conference-box p {
  font-size: 14px;
  color: #666;
}
.banner {
  position: relative;
  width: 100vw;
  height: 350px;
  margin-left: calc(-50vw + 50%);
  overflow: hidden;
}

.banner-image{
  width: 100%;
  height: 500px;
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
  font-size: 20px;
  padding: 15px 30px;
  margin: 10px;
  cursor: pointer;
  border: none;
  border-radius: 5px;
}

.login-button {
  background-color: #203641;
  color: white;
}

.login-button:hover {
  background-color: #26e7aa;
}

.signup-button {
  background-color: #579f97;
  color: white;
}

.signup-button:hover {
  background-color: #26e7aa;
}

.info-row {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.info-box {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
  flex: 1;
  max-width: 300px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.icon-circle {
  width: 50px;
  height: 50px;
  margin: 0 auto 10px;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color:#579f97;
  color: #fff;
  border-radius: 50%;
  font-size: 20px;
}

.info-box h3 {
  font-size: 18px;
  margin: 10px 0;
}

.info-box p {
  font-size: 14px;
  color: #666;
}

</style>
