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
/* Add global styles if needed */


#header {
  flex-shrink: 0;
}

#footer {
  flex-shrink: 0;
}

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  width: 100%;
}

#content {
  flex-grow: 1;
  width: 100%;
  padding: 0; /* Ensure no internal padding */
}

</style>