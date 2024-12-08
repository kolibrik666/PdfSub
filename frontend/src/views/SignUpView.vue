<template>
    <div class="sign-up">
        <DisplayCard :isSignUp="true" />
    </div>
  </template>
  
  <script>
  // @ is an alias to /src
  import DisplayCard from '@/components/DisplayCard.vue';
  
  export default {
    name: 'SignUpView',
    components: {
      DisplayCard,
    }
  }
  </script>
  