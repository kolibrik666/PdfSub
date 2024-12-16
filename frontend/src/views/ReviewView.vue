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
          { name: 'Aktuálnosť a náročnosť práce', options: ['D', 'E', 'Fx', 'A'] },
          { name: 'Rozsah a úroveň dosiahnutých výsledkov', options: ['D', 'E', 'Fx', 'A'] },
          { name: 'Analýza a interpretácia výsledkov a formulácia záveru práce', options: ['D', 'E', 'Fx', 'A'] },
          { name: 'Prehľadnosť a logická štruktúra práce', options: ['D', 'E', 'Fx', 'A'] },
          { name: 'Formálna, jazyková a štylistická úprava práce', options: ['D', 'E', 'Fx', 'A'] },
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
      };
    },
    methods: {
  submitReview() {
    const reviewData = {
      publicationId: this.$route.params.id, // Get the ID from the route
      review: this.review,
    };

    // Call the API to submit the review
    api.submitReview(reviewData)
      .then(() => {
        alert('Review submitted successfully!');
        this.$router.push('/publications'); // Redirect back to the main page or another desired page
      })
      .catch(error => {
        console.error('Error submitting review:', error);
        alert('Failed to submit review.');
      });
  },
},

  };
  </script>
  
  