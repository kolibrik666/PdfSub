<template>
  <div class="filters">
    <input v-model="localFilterQuery" type="text" placeholder="Search by title..." @input="emitFilters" />
    <select v-model="localFilterStatus" @change="emitFilters">
      <option value="">All Statuses</option>
      <option value="pending">Pending</option>
      <option value="reviewed">Reviewed</option>
    </select>
    <select v-model="localFilterConference" @change="emitFilters">
      <option value="">All Conferences</option>
      <option v-for="conference in conferences" :key="conference._id" :value="conference._id">
        {{ conference.name }}
      </option>
    </select>
  </div>
</template>

<script>
export default {
  props: {
    conferences: {
      type: Array,
      required: true,
    },
    initialFilters: {
      type: Object,
      default: () => ({
        query: "",
        status: "",
        conference: "",
      }),
    },
  },
  data() {
    return {
      localFilterQuery: this.initialFilters.query,
      localFilterStatus: this.initialFilters.status,
      localFilterConference: this.initialFilters.conference,
    };
  },
  methods: {
    emitFilters() {
      this.$emit("filter-change", {
        query: this.localFilterQuery,
        status: this.localFilterStatus,
        conference: this.localFilterConference,
      });
    },
  },
};
</script>

<style scoped>
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filters input,
.filters select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
</style>
