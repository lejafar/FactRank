<template>
	<div>
		<b-form>
		<b-nav-form @submit="onSubmit">
			<b-form-input v-model="search_query" class="mr-sm-2 search" placeholder="Search"></b-form-input>
			<b-button variant="outline-success" class="my-2 my-sm-0" type="submit">Search</b-button>
		</b-nav-form>
		</b-form>
		<results-table v-bind:results="search_results"/>
	</div>
</template>

<script>
import ResultsTable from './ResultsTable'

export default {
  name: 'Search',
  data () {
      return {
        search_results: [],
		search_query: ''
      }
  },
  methods: {
    fetchSearchResults (query) {
        fetch("https://api-v2.factrank.org/search", {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({'q': query}),
        }).then(response => response.json()).then((data) => {
          this.search_results = data
      });
    },
	onSubmit(evt) {
		evt.preventDefault();
		this.search_results = []
		this.fetchSearchResults(this.search_query)
	},
  },
  components: {
    'results-table': ResultsTable
  },
  mounted() {
    this.fetchSearchResults ()
  }
}
</script>

<style scoped>
form {
    margin-bottom: 1rem;
}
input.search {
	margin-left: auto;
}
</style>
