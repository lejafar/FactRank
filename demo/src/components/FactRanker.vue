<template>
    <results-table v-bind:result="result"/>
</template>

<script>
import ResultsTable from './ResultsTable'

export default {
  name: 'FactRanker',
  data () {
      return {
        result: {}
      }
  },
  methods: {
    fetchPrediction () {
        fetch("https://api.factrank.org/" + this.$api_version + "/plenair")
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
