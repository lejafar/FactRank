<template>
    <b-table
            v-if="search_results"
            :fields="fields"
            :items="search_results"
            caption-top>

      <!-- A virtual column -->
      <template slot="index" slot-scope="data">
        {{ data.index + 1 }}
      </template>

    </b-table>
    <div v-else class="loader-container">
      <rotate-loader :color="'#ffc107'"></rotate-loader>
    </div>
</template>

<script>
import RotateLoader from 'vue-spinner/src/RotateLoader'

export default {
  name: 'SearchResultsTable',
  props: ['search_results'],
  components: {
    'rotate-loader': RotateLoader
  },
  data () {
    return {
      fields: [
        { key: 'index', label: '#'},
        // A column that needs custom formatting
        { key: 'content', label: 'Statement'},
      ],
    }
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
</style>
