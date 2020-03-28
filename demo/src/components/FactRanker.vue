<template>
  <div>
    <b-form inline @submit="onSubmit">
      <label class="mr-sm-2" for="inline-form-custom-select-source">
        Check-Worthy Factual Statements from
      </label>
      <b-form-select
        class="mb-2 mr-sm-2 mb-sm-0"
        v-model="source_type"
        @change="resetPageAndFetchTopCheckWorthy"
        :options="source_options"
        id="inline-form-custom-select-source"
      >
      </b-form-select>

      <label class="mr-sm-2" for="inline-form-custom-select-country">
        made by
      </label>
      <b-form-select
        class="mb-1 mr-sm-1 mb-sm-0"
        v-model="speaker_country"
        @change="resetPageAndFetchTopCheckWorthy"
        :options="country_options"
        id="inline-form-custom-select-country"
      ></b-form-select>
      <label class="mr-sm-2" for="inline-form-custom-select-country">
        speaker,
      </label>

      <label class="mr-sm-2" for="inline-form-custom-select-time">
        during
      </label>
      <b-form-select
        class="mb-2 mr-sm-2 mb-sm-0"
        @change="resetPageAndFetchTopCheckWorthy"
        v-model="top_last"
        :options="options"
        id="inline-form-custom-select-time"
      ></b-form-select>
      <label class="mr-sm-2" for="inline-form-custom-select-time">
        sort by
      </label>
      <b-form-select
        class="mb-2 mr-sm-2 mb-sm-0"
        @change="resetPageAndFetchTopCheckWorthy"
        v-model="sort_by"
        :options="sort_options"
        id="inline-form-custom-select-time"
      ></b-form-select>
    </b-form>
    <b-form @submit="onSubmit">
      <label class="search-glass" for="inline-form-custom-select-search"
        ><icon name="search" scale="1"
      /></label>
      <b-form-input
        class="search"
        v-model="search_query"
        placeholder="Search"
        type="search"
        id="inline-form-custom-select-search"
      ></b-form-input>

    </b-form>
    <results-table
      v-bind:results="top_results"
      :model_version="model_version"
      :debug="debug"
      :page="currentPage"
      :limit="limit"
    />
    <b-pagination
      v-if="top_results"
      v-model="currentPage"
      :total-rows="rows"
      :per-page="limit"
      :limit="15"
      @input="fetchTopCheckWorthy"
      align="center"
      pills
    ></b-pagination>
  </div>
</template>

<script>
import ResultsTable from "./ResultsTable";

export default {
  name: "Search",
  data() {
    return {
      top_results: null,
      options: [
        { value: "day", text: "last 24h" },
        { value: "week", text: "last week" },
        { value: "month", text: "last month" },
        { value: "year", text: "last year" },
        { value: "", text: "all time" },
      ],
      country_options: [
        { value: "", text: "🇧🇪/🇳🇱" },
        { value: "BE", text: "🇧🇪" },
        { value: "NL", text: "🇳🇱" },
      ],
      source_options: [
        { value: "", text: "All sources" },
        {
            label: 'Social',
            options: [
            { value: "TWITTER", text: "Twitter" },
            ]
        },
        {
            label: 'Parliament',
            options: [
            { value: "FLEMISH_PARLIAMENTARY_MEETING", text: "Flemish Parliament" },
            { value: "BELGIAN_PARLIAMENTARY_MEETING", text: "Belgian Parliament" },
            { value: "DUTCH_PARLIAMENTARY_MEETING", text: "Dutch Parliament" }
            ]
        },
        {
            label: 'Subtitles',
            options: [
                { value: "VRT_TERZAKE", text: "Terzake" },
                { value: "VRT_DE_AFSPRAAK", text: "De Afspraak" },
            ]
        },
        {
            label: 'FactCheckers',
            options: [
                { value: "FACTCHECK_VLAANDEREN", text: "FactCheck Flanders" },
                { value: "NIEUWSCHECKERS", text: "NieuwsCheckers" },
            ]
        },
      ],
      sort_options: [
        { value: "", text: "relevance" },
        { value: "time", text: "time" },
        { value: "score", text: "score" },
      ],
      model_version: "v0.6.0",
      model_versions: [],
      debug: false,
      top_last: "",
      speaker_country: "",
      source_type: "",
      search_query: "",
      sort_by: "",
      limit: 30,
      currentPage: 1,
      rows: 0,
    };
  },
  methods: {
    fetchModelVersions() {
      fetch("https://api-v2.factrank.org/models", {
        method: "GET",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          this.model_versions = data.map(function (model_version) {
            return {
              value: model_version.name,
              text: model_version.name,
              id: model_version.id,
            };
          });
        });
    },
    pushOptionsToQuery() {
      var q = {
        type: this.source_type,
        country: this.speaker_country,
        limit: this.top_last,
        q: this.search_query,
        page: this.currentPage,
        sort: this.sort_by
      };
      q = Object.fromEntries(Object.entries(q).filter(([_, v]) => v != "" && v != 1));
      this.$router.push({ query: q });
    },
    resetPageAndFetchTopCheckWorthy(){
       this.currentPage = 1;
       this.fetchTopCheckWorthy();
    },
    fetchTopCheckWorthy() {
      // fix some incompatibilities
      if ( this.source_type != "TWITTER"){
        this.speaker_country = "";
      }

      this.top_results = null;
      this.pushOptionsToQuery();
      fetch(this.$api_url + "/search", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          top_last: this.top_last,
          version: this.model_version,
          limit: this.limit,
          page: this.currentPage,
          source_type: this.source_type,
          speaker_country: this.speaker_country,
          q: this.search_query,
          sort: this.sort_by
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.top_results = data.results;
          this.rows = data.total;
        });
    },
    onSubmit(evt) {
      this.currentPage = 1;
      evt.preventDefault();
      this.fetchTopCheckWorthy();
    },
  },
  components: {
    "results-table": ResultsTable,
  },
  mounted() {
    (this.top_last =
      "limit" in this.$route.query ? this.$route.query.limit : ""),
      (this.speaker_country =
        "country" in this.$route.query ? this.$route.query.country : ""),
      (this.source_type =
        "type" in this.$route.query ? this.$route.query.type : ""),
      (this.search_query = "q" in this.$route.query ? this.$route.query.q : ""),
      (this.sort_by =
        "sort" in this.$route.query ? this.$route.query.sort : ""),
      (this.currentPage =
        "page" in this.$route.query ? parseInt(this.$route.query.page) : 1),
      (this.debug = this.$route.query.debug || false);
    this.fetchTopCheckWorthy();
  },
};
</script>

<style scoped>
form {
  margin-bottom: 1rem;
}
label,
label.search-glass {
  display: none;
}
@media (min-width: 768px) {
  input.search {
    width: 95%;
  }
}
@media (min-width: 576px) {
  .form-inline .input-group,
  .form-inline .custom-select {
    font-weight: bold;
    border: 0px solid #ced4da;
    border-bottom: 1px dotted #ced4da;
    border-radius: 0px;
  }
  label,
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
  input:focus,
  select:focus {
    border: 0;
    border-bottom: 1px dotted #ced4da;
    -webkit-box-shadow: none;
    -moz-box-shadow: none;
    box-shadow: none;
  }
}
</style>
