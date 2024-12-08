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
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

#header {
  flex-shrink: 0;
}

#content {
  flex-grow: 1;
}

#footer {
  flex-shrink: 0;
}
</style>