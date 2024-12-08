<template>
    <div class="login">
        <DisplayCard :isSignUp="false" />
    </div>
  </template>
  
  <script>
  // @ is an alias to /src
  import DisplayCard from '@/components/DisplayCard.vue';
  
  export default {
    name: 'LoginView',
    components: {
      DisplayCard,
    }
  }
  </script>
  