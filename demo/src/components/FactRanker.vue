<template>
    <div>
        <b-form-group label-cols="8" label-cols-lg="4" label-size="sm" label="Top Check-Worthy Factual Statement of" label-for="input-sm">
                <b-form-select @change="fetchTopCheckWorthy" v-model="top_last" :options="options"></b-form-select>
        </b-form-group>
        <results-table v-bind:results="top_results"/>
    </div>
</template>

<script>
import ResultsTable from './ResultsTable'

export default {
    name: 'Search',
    data () {
        return {
            top_results: null,
            top_last: 'month',
            options: [
                { value: 'hour', text: 'last hour' },
                { value: 'day', text: 'last 24h' },
                { value: 'week', text: 'last week' },
                { value: 'month', text: 'last month' },
                { value: 'year', text: 'last year' },
                { value: 'all_time', text: 'all time' },
            ]
        }
    },
    methods: {
        fetchTopCheckWorthy () {
            this.top_results = null
            fetch("https://api-v2.factrank.org/search", {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'top_last': this.top_last, 'limit': 100}),
            }).then(response => response.json()).then((data) => {
                this.top_results = data
            });
        },
    },
    components: {
        'results-table': ResultsTable
    },
    mounted() {
        this.fetchTopCheckWorthy ()
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
