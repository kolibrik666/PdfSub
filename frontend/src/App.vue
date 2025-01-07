<template>
  <div id="app">
    <section id="header">
      <Navigation />
    </section>

    <!-- Main Content -->
    <section id="content">
      <router-view />
    </section>

    <section id="footer">
      <Footer />
    </section>
  </div>
</template>

<script>
import Navigation from './components/TheNavigation.vue';
import Footer from './components/TheFooter.vue';

export default {
  components: {
    Navigation,
    Footer,
  },
};
</script>
<style>
#header {
  flex-shrink: 0;
}

#footer {
  flex-shrink: 0;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

#content {
  flex-grow: 1;
  width: 90%;
  margin: 0 auto; /* Horizontally center the content */
  padding: 0;
}
</style>

