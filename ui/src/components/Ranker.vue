<template>
  <div>
    <div v-if="!demo">
      <b-form inline @submit="onSubmit">
        <label class="mr-sm-2" for="inline-form-custom-select-source">
          {{ $t("factranker.filters.checkWorthyStatementsFrom") }}
        </label>
        <b-form-select
          class="mb-2 mr-sm-2 mb-sm-0"
          v-model="source_type"
          @change="resetPageAndFetchTopCheckWorthy"
          :options="source_options"
          :disabled="demo"
          id="inline-form-custom-select-source"
        ></b-form-select>

        <label class="mr-sm-2" for="inline-form-custom-select-country">
          {{ $t("factranker.filters.madeBy") }}
        </label>
        <b-form-select
          class="mb-1 mr-sm-1 mb-sm-0"
          v-model="speaker_country"
          @change="resetPageAndFetchTopCheckWorthy"
          :options="country_options"
          :disabled="demo || no_country"
          id="inline-form-custom-select-country"
        ></b-form-select>
        <label class="mr-sm-2" for="inline-form-custom-select-country">
          {{ $t("factranker.filters.speaker") }},
        </label>

        <label class="mr-sm-2" for="inline-form-custom-select-time">
          {{ $t("factranker.filters.during") }},
        </label>
        <b-form-select
          class="mb-2 mr-sm-2 mb-sm-0"
          @change="resetPageAndFetchTopCheckWorthy"
          v-model="top_last"
          :options="options"
          :disabled="demo"
          id="inline-form-custom-select-time"
        ></b-form-select>

        <label class="mr-sm-2" for="inline-form-custom-select-time">
          {{ $t("factranker.filters.sortBy") }}
        </label>
        <b-form-select
          class="mb-2 mr-sm-2 mb-sm-0"
          @change="resetPageAndFetchTopCheckWorthy"
          v-model="sort_by"
          :options="sort_options"
          :disabled="demo"
          id="inline-form-custom-select-time"
        ></b-form-select>
      </b-form>

      <b-form @submit="onSubmit">
        <label class="search-glass" for="inline-form-custom-select-search">
          <icon name="search" scale="1" />
        </label>
        <b-form-input
          class="search"
          v-model="search_query"
          :placeholder="$t('factranker.filters.search')"
          type="search"
          :disabled="demo"
          id="inline-form-custom-select-search"
        ></b-form-input>
      </b-form>
    </div>
    <results-table
      v-bind:results="top_results"
      :model_version="model_version"
      :debug="debug"
      :page="currentPage"
      :limit="limit"
    />
    <b-pagination
      v-if="top_results && !demo"
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
  name: "Ranker",
  props: {
    limit: {
      type: Number,
      default: 30,
    },
    top_last: {
      type: String,
      default: "",
    },
    speaker_country: {
      type: String,
      default: "",
    },
    source_type: {
      type: String,
      default: "",
    },
    search_query: {
      type: String,
      default: "",
    },
    sort_by: {
      type: String,
      default: "",
    },
    demo: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      top_results: null,
      options: [
        {
          value: "day",
          text: this.$t("factranker.filters.limit.last24Hours"),
        },
        {
          value: "week",
          text: this.$t("factranker.filters.limit.lastWeek"),
        },
        {
          value: "month",
          text: this.$t("factranker.filters.limit.lastMonth"),
        },
        {
          value: "year",
          text: this.$t("factranker.filters.limit.lastYear"),
        },
        {
          value: "",
          text: this.$t("factranker.filters.limit.allTime"),
        },
      ],
      country_options: [
        {
          value: "",
          text: "🇧🇪/🇳🇱",
        },
        {
          value: "BE",
          text: "🇧🇪",
        },
        {
          value: "NL",
          text: "🇳🇱",
        },
      ],
      no_country: false,
      source_options: [
        {
          value: "",
          text: this.$t("factranker.filters.source.allSources"),
        },
        {
          label: this.$t("factranker.filters.source.social"),
          options: [
            {
              value: "TWITTER",
              text: this.$t("factranker.filters.source.twitter"),
            },
          ],
        },
        {
          label: this.$t("factranker.filters.source.parliament"),
          options: [
            {
              value: "FLEMISH_PARLIAMENTARY_MEETING",
              text: this.$t("factranker.filters.source.flemishParliament"),
            },
            {
              value: "BELGIAN_PARLIAMENTARY_MEETING",
              text: this.$t("factranker.filters.source.belgianParliament"),
            },
            {
              value: "DUTCH_PARLIAMENTARY_MEETING",
              text: this.$t("factranker.filters.source.dutchParliament"),
            },
          ],
        },
        {
          label: this.$t("factranker.filters.source.subtitles"),
          options: [
            {
              value: "VRT_TERZAKE",
              text: this.$t("factranker.filters.source.terzake"),
            },
            {
              value: "VRT_DE_AFSPRAAK",
              text: this.$t("factranker.filters.source.deAfspraak"),
            },
          ],
        },
        {
          label: this.$t("factranker.filters.source.factcheckers"),
          options: [
            {
              value: "FACTCHECK_VLAANDEREN",
              text: this.$t("factranker.filters.source.factcheckFlanders"),
            },
            {
              value: "NIEUWSCHECKERS",
              text: this.$t("factranker.filters.source.nieuwscheckers"),
            },
            {
              value: "KNACK_FACTCHECK",
              text: this.$t("factranker.filters.source.knackFactcheck"),
            },
          ],
        },
      ],
      sort_options: [
        {
          value: "",
          text: this.$t("factranker.filters.sort.relevance"),
        },
        {
          value: "time",
          text: this.$t("factranker.filters.sort.time"),
        },
        {
          value: "score",
          text: this.$t("factranker.filters.sort.score"),
        },
      ],
      model_version: "v0.6.0",
      model_versions: [],
      debug: false,
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
        sort: this.sort_by,
      };
      q = Object.fromEntries(
        Object.entries(q).filter(([, v]) => v != "" && v != 1)
      );
      this.$router.push({
        query: q,
      });
    },
    resetPageAndFetchTopCheckWorthy() {
      this.currentPage = 1;
      this.fetchTopCheckWorthy();
    },
    fetchTopCheckWorthy() {
      // fix some incompatibilities
      if (this.source_type == "TWITTER" || this.source_type == "") {
        this.no_country = false;
      } else {
        if (this.source_type.includes("BELGIAN") || this.source_type.includes("FLEMISH")) {
            this.speaker_country = "BE";
        }
        else if (this.source_type.includes("DUTCH")) {
            this.speaker_country = "NL";
        }
        else {
            this.speaker_country = "";
        }
        this.no_country = true;
      }

      this.top_results = null;
      !this.demo && this.pushOptionsToQuery();
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
          sort: this.sort_by,
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
    if (!this.demo) {
      (this.top_last =
        "limit" in this.$route.query ? this.$route.query.limit : ""),
        (this.speaker_country =
          "country" in this.$route.query ? this.$route.query.country : ""),
        (this.source_type =
          "type" in this.$route.query ? this.$route.query.type : ""),
        (this.search_query =
          "q" in this.$route.query ? this.$route.query.q : ""),
        (this.sort_by =
          "sort" in this.$route.query ? this.$route.query.sort : ""),
        (this.currentPage =
          "page" in this.$route.query ? parseInt(this.$route.query.page) : 1),
        (this.debug = this.$route.query.debug || false);
    }
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
@media (min-width: 576px) {
    #inline-form-custom-select-country {
        border-radius: 5px;
    }
}
</style>
