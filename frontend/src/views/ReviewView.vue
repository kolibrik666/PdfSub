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
        console.log('Review submitted:', this.review);
        // Handle the form submission logic here, like sending it to the backend
      },
    },
  };
  </script>
  
  <style scoped>
  .review-view {
    padding: 20px;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
  }
  
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
  }
  
  th {
    background-color: #f2f2f2;
  }
  
  button {
    margin-top: 20px;
  }
  
  
textarea {
  width: 96%;
  padding: 8px;
  border: 1px solid #ddd;
  resize: vertical; 
}
  
  label {
    margin-right: 10px;
  }
  </style>
  