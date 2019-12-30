<template>
    <div>
	<b-form inline @submit="onSubmit">
        <label class="mr-sm-2" for="inline-form-custom-select-source">Check-Worthy Factual Statements from</label>
		<b-form-select
		class="mb-2 mr-sm-2 mb-sm-0"
		v-model="source_type"
		@change="fetchTopCheckWorthy"
		:options="{ '': 'All sources', 'TWITTER': 'Twitter', 'FLEMISH_PARLIAMENTARY_MEETING': 'Flemish Parliament', 'BELGIAN_PARLIAMENTARY_MEETING': 'Belgian Parliament', 'DUTCH_PARLIAMENTARY_MEETING': 'Dutch Parliament'}"
		id="inline-form-custom-select-source"
		>
		</b-form-select>

        <label class="mr-sm-2" for="inline-form-custom-select-country">made by</label>
		<b-form-select
		class="mb-1 mr-sm-1 mb-sm-0"
		v-model="speaker_country"
		@change="fetchTopCheckWorthy"
		:options="{ '': '🇧🇪/🇳🇱',
                  'BE': '🇧🇪',
                  'NL': '🇳🇱'}"
		id="inline-form-custom-select-country"
		></b-form-select>
        <label class="mr-sm-2" for="inline-form-custom-select-country">speaker, </label>

        <label class="mr-sm-2" for="inline-form-custom-select-time">during</label>
        <b-form-select
        class="mb-2 mr-sm-2 mb-sm-0"
        @change="fetchTopCheckWorthy"
        v-model="top_last"
        :options="options"
        id="inline-form-custom-select-time"
        ></b-form-select>

	</b-form>
	<b-form @submit="onSubmit">
        <label class="search-glass" for="inline-form-custom-select-search"><icon name="search" scale="1"/></label>
		<b-form-input
		class="search"
		v-model="search_query"
		placeholder="Search"
		type="search"
		id="inline-form-custom-select-search"
		></b-form-input>
	</b-form>
        <!--<b-form inline>-->
            <!--<label class="mr-sm-2" for="inline-form-custom-select-pref">Top Check-Worthy Factual Statement of</label>-->
        <!--<b-form-group label-cols="8" label-cols-lg="4" label-size="sm" label="Top Check-Worthy Factual Statement of" label-for="input-sm">-->
            <!--<b-form-select class="mb-2 mr-sm-2 mb-sm-0" @change="fetchTopCheckWorthy" v-model="top_last" :options="options"></b-form-select>-->
            <!--<b-form-select class="mb-2 mr-sm-2 mb-sm-0" @change="fetchTopCheckWorthy" v-model="model_version" :options="model_versions"></b-form-select>-->
        <!--</b-form>-->
        <!--</b-form-group>-->
        <results-table v-bind:results="top_results" :model_version="model_version" :debug="debug"/>
    </div>
</template>

<script>
import ResultsTable from './ResultsTable'

export default {
    name: 'Search',
    data () {
        return {
            top_results: null,
            options: [
                { value: 'day', text: 'last 24h' },
                { value: 'week', text: 'last week' },
                { value: 'month', text: 'last month' },
                { value: 'year', text: 'last year' },
                { value: '', text: 'all time' },
            ],
            model_version: 'v0.5.0',
            model_versions: [],
            debug: false,
			top_last: '',
			speaker_country: '',
			source_type: '',
			search_query: '',
        }
    },
    methods: {
        fetchModelVersions() {
            fetch("https://api-v2.factrank.org/models", {
                method: 'GET',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
            }).then(response => response.json()).then((data) => {
                this.model_versions = data.map(function (model_version) { return { value: model_version.name, text: model_version.name, id: model_version.id} });
            });

        },
        fetchTopCheckWorthy () {
            this.top_results = null;
            var q = {type: this.source_type, country: this.speaker_country, limit: this.top_last, q: this.search_query};
            q = Object.fromEntries(Object.entries(q).filter(([_,v]) => v != ''));
            this.$router.push({query: q});
            fetch(this.$api_url + "/search", {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({'top_last': this.top_last, 'version': this.model_version, 'limit': 100, 'source_type': this.source_type, 'speaker_country': this.speaker_country, 'q': this.search_query}),
            }).then(response => response.json()).then((data) => {
                this.top_results = data
            });
        },
		onSubmit(evt) {
			evt.preventDefault();
			this.fetchTopCheckWorthy();
		},
    },
    components: {
        'results-table': ResultsTable
    },
    mounted() {
		this.top_last = 'limit' in this.$route.query ? this.$route.query.limit : '',
		this.speaker_country='country' in this.$route.query ? this.$route.query.country : '',
		this.source_type= 'type' in this.$route.query ? this.$route.query.type : '',
		this.search_query= 'q' in this.$route.query ? this.$route.query.q : '',
        this.debug = this.$route.query.debug || false
        this.fetchTopCheckWorthy ()
    }
}
</script>

<style scoped>
form {
    margin-bottom: 1rem;
}
label.search-glass {
	display: none;
}
@media (min-width: 768px) {
	input.search {
		width: 95%;
	}
}
@media (min-width: 576px){
	.form-inline .input-group, .form-inline .custom-select {
		font-weight: bold;
		border: 0px solid #ced4da;
		border-bottom: 1px dotted #ced4da;
		border-radius: 0px;
	}
	label.search-glass {
		display: inline-block;
	}
	input.search {
		font-weight: bold;
		border: 0px solid #ced4da;
		border-bottom: 1px dotted #ced4da;
		border-radius: 0px;
		display: inline-block;
		width: 90%;
		margin-left: 2.5%;
		}
}

</style>
