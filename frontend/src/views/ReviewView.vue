<template>
  <div class="review-view">
    <h2><i class="fa-solid fa-file-pen"></i> Paper Review</h2>
    <h1 class="green-text">{{ publicationName }}</h1>
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
                  required
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
import api from "../services/api";

export default {
  data() {
    const criteria = [
      {
        name: "Aktuálnosť a náročnosť práce",
        options: ["A", "B", "C", "D", "E", "Fx"],
      },
      {
        name: "Zorientovanie sa študenta v danej problematike prostredníctvom analýzou domácej a zahraničnej literatúry",
        options: ["A", "B", "C", "D", "E", "Fx"],
      },
      {
        name: "Vhodnosť zvolených metód spracovania riešenej problematiky",
        options: ["A", "B", "C", "D", "E", "Fx"],
      },
      {
        name: "Rozsah a úroveň dosiahnutých výsledkov",
        options: ["A", "B", "C", "D", "E", "Fx"],
      },
      {
        name: "Analýza a interpretácia výsledkov a formulácia záverov práce",
        options: ["A", "B", "C", "D", "E", "Fx"],
      },
      {
        name: "Prehľadnosť a logická štruktúra práce",
        options: ["A", "B", "C", "D", "E", "Fx"],
      },
      {
        name: "Formálna, jazyková a štylistická úroveň práce",
        options: ["A", "B", "C", "D", "E", "Fx"],
      },
      {
        name: "Práca zodpovedá šablóne určenej pre ŠVK",
        options: ["áno", "nie"],
      },
      {
        name: "Chýba názov práce v slovenskom alebo anglickom jazyku",
        options: ["áno", "nie"],
      },
      { name: "Chýba meno autora alebo školiteľa", options: ["áno", "nie"] },
      {
        name: "Chýba pracovná emailová adresa autora alebo školiteľa",
        options: ["áno", "nie"],
      },
      {
        name: "Chýba abstrakt v slovenskom alebo anglickom jazyku",
        options: ["áno", "nie"],
      },
      { name: "Abstrakt nespĺňa rozsah 100–150 slov", options: ["áno", "nie"] },
      {
        name: "Chýbajú kľúčové slová v slovenskom alebo anglickom jazyku",
        options: ["áno", "nie"],
      },
      {
        name: "Chýba „Úvod“, „Výsledky a diskusia“ alebo „Záver“",
        options: ["áno", "nie"],
      },
      {
        name: "Nie sú uvedené zdroje a použitá literatúra",
        options: ["áno", "nie"],
      },
      {
        name: "V texte chýbajú referencie na zoznam bibliografie",
        options: ["áno", "nie"],
      },
      {
        name: "V texte chýbajú referencie na použité obrázky a/alebo tabuľky",
        options: ["áno", "nie"],
      },
      {
        name: "Obrázkom a/alebo tabuľkám chýba popis",
        options: ["áno", "nie"],
      },
      {
        name: "Prácu odporúčam",
        options: [
          "publikovať",
          "publikovať po zapracovaní pripomienok",
          "neprijať pre publikovanie",
        ],
      },
    ];

    const review = {};
    criteria.forEach((criterion) => {
      review[criterion.name] = ""; // Initialize with empty strings or a default value
    });

    return {
      criteria,
      review,
      reviewerId: "",
      publicationName: "",
    };
  },
  methods: {
    fetchReviewData() {
      const publicationId = this.$route.params.id;
      api
        .getPublication(publicationId)
        .then((response) => {
          const existingReview = response.data.review_data || {};
          this.review = { ...this.review, ...existingReview };
          this.reviewerId = response.data.reviewerId || "";
          this.publicationName = response.data.title || "";
        })
        .catch((error) => {
          console.error("Error fetching review data:", error);
          alert("Failed to load existing review data.");
        });
    },
    submitReview() {
      const review_data = JSON.parse(JSON.stringify(this.review));
      const data = {
        reviewerId: this.reviewerId,
        review_data: review_data,
        review_status: "reviewed",
      };

      api
        .updatePublication(this.$route.params.id, data)
        .then(() => {
          alert("Review submitted successfully!");
          this.$router.push("/publications");
        })
        .catch((error) => {
          console.error("Error submitting review:", error);
          alert("Failed to submit review.");
        });
    },
  },
  mounted() {
    this.fetchReviewData();
  },
};
</script>
