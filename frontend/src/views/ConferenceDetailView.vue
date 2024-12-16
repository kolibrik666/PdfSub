<template>
  <div v-if="conference">
    <h1>{{ conference.name }}</h1>
    <p><strong>Date:</strong> {{ conference.date }}</p>

    <h2>Users</h2>
    <ul>
      <li v-for="participant in conference.users" :key="participant">
        {{ participant }}
      </li>
    </ul>

    <h2>Papers</h2>
    <ul>
      <li v-for="paper in conference.papers" :key="paper">
        {{ paper }}
      </li>
    </ul>

    <router-link to="/conferences">Back to Conferences</router-link>
  </div>
</template>

<script>
import api from "@/services/api";

export default {
  data() {
    return {
      conference: null,
    };
  },
  methods: {
    fetchConferenceDetails() {
      const id = this.$route.params.id;
      api.getConferenceDetails(id)
          .then((response) => {
            this.conference = response.data;
          })
          .catch((error) => {
            console.error("Error fetching conference details:", error);
          });
    },
  },
  created() {
    this.fetchConferenceDetails();
  },
};
</script>
