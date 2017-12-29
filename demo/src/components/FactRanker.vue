<template>
  <main>
    <results-table v-bind:result="result"/>
  </main>
</template>

<script>
import ResultsTable from '@/components/ResultsTable'
import VueMarkdown from 'vue-markdown'

export default {
  name: 'FactRanker',
  data () {
      return {
        result: {}
      }
  },
  methods: {
    fetchPrediction (tag) {
      fetch("https://api.factrank.org/plenair")
        .then(response => response.json())
        .then((data) => {
          this.result = data
      })
    }
  },
  components: {
    'results-table': ResultsTable
  },
  mounted() {
    this.fetchPrediction ('last')
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
