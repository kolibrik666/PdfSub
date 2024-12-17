<template>
  <div class="review-view">
    <h1>Paper Review</h1>
    <form @submit.prevent="submitReview">
      <table>
        <thead>
        <tr>
          <th>Criteria</th>
          <th>Rating</th>
        </tr>
        </thead>
        <tbody>
        <!-- Loop through the existing criteria with radio buttons -->
        <tr v-for="(criterion, index) in criteria" :key="index">
          <td>{{ criterion.name }}</td>
          <td>
            <label v-for="(option, i) in criterion.options" :key="i">
              <input
                  type="radio"
                  :name="criterion.name"
                  :value="option"
                  v-model="review[criterion.name]"
              />
              {{ option }}
            </label>
          </td>
        </tr>

        <tr>
          <td>Silné stránky práce</td>
          <td>
              <textarea
                  v-model="review['Silné stránky práce']"
                  placeholder="Enter strengths of the paper"
                  rows="5"
              ></textarea>
          </td>
        </tr>

        <tr>
          <td>Slabé stránky práce</td>
          <td>
              <textarea
                  v-model="review['Slabé stránky práce']"
                  placeholder="Enter weaknesses of the paper"
                  rows="5"
              ></textarea>
          </td>
        </tr>
        </tbody>
      </table>

      <button type="submit">Submit Review</button>
    </form>
  </div>
</template>

<script>
import api from '../services/api';

export default {
  data() {
    return {
      criteria: [
        { name: 'Aktuálnosť a náročnosť práce', options: ['A', 'B', 'C' ,'D', 'E', 'Fx'] },
        { name: 'Rozsah a úroveň dosiahnutých výsledkov', options: ['A', 'B', 'C' ,'D', 'E', 'Fx'] },
        { name: 'Analýza a interpretácia výsledkov a formulácia záveru práce', options: ['A', 'B', 'C' ,'D', 'E', 'Fx'] },
        { name: 'Prehľadnosť a logická štruktúra práce', options: ['A', 'B', 'C' ,'D', 'E', 'Fx'] },
        { name: 'Formálna, jazyková a štylistická úprava práce', options: ['A', 'B', 'C' ,'D', 'E', 'Fx'] },
        { name: 'Chýba názov práce v slovenskom alebo anglickom jazyku', options: ['áno', 'nie'] },
        { name: 'Chýba meno autora alebo školiteľa', options: ['áno', 'nie'] },
        { name: 'Chýba pracovná emailová adresa autora alebo školiteľa', options: ['áno', 'nie'] },
        { name: 'Chýba abstrakt v slovenskom alebo anglickom jazyku', options: ['áno', 'nie'] },
      ],
      review: {
        'Aktuálnosť a náročnosť práce': '',
        'Rozsah a úroveň dosiahnutých výsledkov': '',
        'Analýza a interpretácia výsledkov a formulácia záveru práce': '',
        'Prehľadnosť a logická štruktúra práce': '',
        'Formálna, jazyková a štylistická úprava práce': '',
        'Chýba názov práce v slovenskom alebo anglickom jazyku': '',
        'Chýba meno autora alebo školiteľa': '',
        'Chýba pracovná emailová adresa autora alebo školiteľa': '',
        'Chýba abstrakt v slovenskom alebo anglickom jazyku': '',
        'Silné stránky práce': '',
        'Slabé stránky práce': '',
      },
      reviewerId: '',
    };
  },
  methods: {
    fetchReviewData() {
      const publicationId = this.$route.params.id;
      api.getPublication(publicationId)
          .then(response => {
            const existingReview = response.data.review_data || {};
            this.review = { ...this.review, ...existingReview };
            this.reviewerId = response.data.reviewerId || '';
          })
          .catch(error => {
            console.error('Error fetching review data:', error);
            alert('Failed to load existing review data.');
          });
    },
    submitReview() {
      const review_data = JSON.parse(JSON.stringify(this.review));
      const payload = {
        reviewerId: this.reviewerId,
        review_data: review_data,
      };

      api.updatePublication(this.$route.params.id, payload)
          .then(() => {
            alert('Review submitted successfully!');
            this.$router.push('/publications');
          })
          .catch(error => {
            console.error('Error submitting review:', error);
            alert('Failed to submit review.');
          });
    },
  },
  mounted() {
    this.fetchReviewData();
  },
};
</script>
