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
      <!-- Informational Row -->
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


      
    </div>
  </div>
</template>

<style scoped>
.banner {
  position: relative;
  width: 100vw;
  height: 350px;
  /* Full screen width */
  margin-left: calc(-50vw + 50%);
  /* Adjust position to center */
  overflow: hidden;
}

.banner-image{

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

.banner-image {
  width: 100%;
  height: 500px;
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