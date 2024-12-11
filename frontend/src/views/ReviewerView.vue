<template>
    <div class="reviewer-view">
      <h1>Assigned Papers</h1>
  
      <!-- Displaying a list of assigned papers -->
      <table>
        <thead>
          <tr>
            <th>Paper Title</th>
            <th>Feedback Deadline</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="paper in papers" :key="paper.id">
       
            <td>{{ paper.title }}</td>
            <td>{{ paper.deadline }}</td>
            <td>{{ paper.status }}</td>
            <td>
              <button @click="downloadPaper(paper.fileUrl)">Download</button>
              <button 
      @click="handleReview(paper)" 
      :disabled="paper.status === 'done'"
    >
      Review
    </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        papers: [
          { id: 1, title: 'Paper 1', deadline: '2024-12-20', status: 'pending', fileUrl: 'path/to/paper1.pdf' },
          { id: 2, title: 'Paper 2', deadline: '2024-12-25', status: 'done', fileUrl: 'path/to/paper2.pdf' },
        ],
      };
    },
    methods: {
        handleReview(paper) {
      if (paper.status === 'pending') {
        this.$router.push('/review/' + paper.id);
      } else {
        this.downloadPaper(paper.fileUrl);
      }
    },
      // Download paper logic
      downloadPaper(fileUrl) {
        const link = document.createElement('a');
        link.href = fileUrl;
        link.download = fileUrl.split('/').pop();
        link.click();
      },
  
      // Change status to "done" after feedback submission
      markFeedbackDone(paperId) {
        const paper = this.papers.find(p => p.id === paperId);
        if (paper) {
          paper.status = 'done';
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .reviewer-view {
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
    margin-right: 5px;
  }
  </style>
  