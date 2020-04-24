<template>
  <div>
    <div class="bg-primary-color secondary-color">
      <b-container class="factrank-info">
        <b-jumbotron>
          <h3>
              <div class="navbar-subtitle" v-html="$t('landing.lead')"></div>
          </h3>
          <ul class="features">
            <li class="yes" v-html='$t("landing.features.monitor")'/>
            <li class="yes" v-html='$t("landing.features.feedback")'/>
            <li class="yes" v-html='$t("landing.features.tool")'/>
            <li class="no" v-html='$t("landing.features.not")'/>
          </ul>
        </b-jumbotron>
        <div class="spacing bg-primary-color" />
      </b-container>
    </div>
    <div class="bg-tertiary-color secondary-color">
      <b-container class="rank-demo-view section">
        <a href="/rank">
          <h2>{{ $t("landing.sections.spotting.title") }}</h2>
        </a>
        <p>{{ $t("landing.sections.spotting.lead") }}</p>
      </b-container>
    </div>
    <b-container class="rank-demo-view">
      <h3 id="subtitles">
        {{ $t("landing.sections.spotting.subsection.subtitles") }}
      </h3>
      <ranker
        :limit="5"
        source_type="VRT_TERZAKE,VRT_DE_AFSPRAAK"
        :demo="true"
      />
      <b-button
        pill
        to="/rank?type=VRT_TERZAKE,VRT_DE_AFSPRAAK"
        variant="outline-primary"
      >
        {{ $t("landing.show-more") }}
      </b-button>
    </b-container>
    <div class="bg-primary-color secondary-color">
      <b-container class="rank-demo-view">
        <h3>{{ $t("landing.sections.spotting.subsection.parliament") }}</h3>
        <ranker
          :limit="5"
          source_type="FLEMISH_PARLIAMENTARY_MEETING,BELGIAN_PARLIAMENTARY_MEETING,DUTCH_PARLIAMENTARY_MEETING"
          :demo="true"
        />
        <b-button
          pill
          to="/rank?type=FLEMISH_PARLIAMENTARY_MEETING,BELGIAN_PARLIAMENTARY_MEETING,DUTCH_PARLIAMENTARY_MEETING"
          variant="outline-primary"
        >
          {{ $t("landing.show-more") }}
        </b-button>
      </b-container>
    </div>
    <b-container class="rank-demo-view">
      <h3>{{ $t("landing.sections.spotting.subsection.social") }}</h3>
      <ranker :limit="5" source_type="TWITTER" :demo="true" />
      <b-button pill to="/rank?type=TWITTER" variant="outline-primary">
        {{ $t("landing.show-more") }}
      </b-button>
    </b-container>
    <div class="bg-primary-color secondary-color">
      <b-container class="rank-demo-view section section-dark">
        <a href="/tool">
          <h2>{{ $t("landing.sections.matching.title") }}</h2>
        </a>
        <p>
          {{
            $t("landing.sections.matching.lead", {
              count: this.factcheck_count,
            })
          }}
        </p>
      </b-container>
    </div>
    <div class="spacing" />
    <api
      sentence_input="Dit is een voorbeeld text, waarin enkele beweringen staan die sterk lijken op reed gepubliceerde fact-checks. 

Zeventig procent van de mensen die asiel aanvragen in Nederland, heeft daar geen recht op. Belgische vrouwen leveren blijkbaar ook 56 procent onbetaald werk. En aan een verslaving aan alcohol sterven meer mensen dan aan tabak."
    />
  </div>
</template>

<script>
import Ranker from "@/components/Ranker";
import Api from "@/components/Api";

export default {
  name: "Landing",
  components: {
    ranker: Ranker,
    api: Api,
  },
  data() {
    return {
      factcheck_count: "",
    };
  },
  methods: {
    fetchFactCheckCount() {
      fetch(this.$api_url + "/search", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          top_last: this.top_last,
          version: "v0.6.0",
          source_type: "FACTCHECK_VLAANDEREN,NIEUWSCHECKERS,KNACK_FACTCHECK",
        }),
      })
        .then((response) => response.json())
        .then((data) => {
          this.factcheck_count = data.total;
        });
    },
  },
  mounted() {
    this.fetchFactCheckCount();
  },
};
</script>

<style scoped>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css");
.jumbotron {
  padding: 4rem 0rem !important;
  background-color: inherit !important;
  max-width: 960px;
}
.jumbotron {
  margin-bottom: 0rem;
}
.factrank-info {
  font-style: italic;
  margin-bottom: 0rem;
}
.rank-demo-view h2 {
  text-align: center;
}
.rank-demo-view a {
  text-decoration: none;
}
.main-content {
  margin-top: 0rem;
}
.navbar-subtitle {
  font-size: 20px;
  margin-top: 1.5rem;
  margin-bottom: 1.5rem;
}
ul.features > li {
  margin: 0.75rem 0rem;
}
li.yes:before,
li.no:before {
  font-family: FontAwesome;
  display: inline-block;
  margin-left: -1.3em; /* same as padding-left set on li */
  width: 1.3em; /* same as padding-left set on li */
}
li.yes:before {
  content: "\f00c"; /* FontAwesome Unicode */
}
li.no:before {
  content: "\f00d"; /* FontAwesome Unicode */
}

li {
  opacity: 0;
  animation: fadeIn 0.9s 1;
  animation-fill-mode: forwards;
}

li:nth-child(1) {
  animation-delay: 0.5s;
}
li:nth-child(2) {
  animation-delay: 1s;
}
li:nth-child(3) {
  animation-delay: 1.5s;
}
li:nth-child(4) {
  animation-delay: 2s;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}
.rank-demo-view {
  padding: 2rem 0rem;
}
.btn-outline-primary {
  color: #1976d2;
  border-color: #1976d2;
  text-decoration: none;
  margin: auto;
  display: block;
  max-width: 120px;
}
.bg-primary-color .btn-outline-primary {
  color: #ffffff;
  border-color: #ffffff;
}
.btn-outline-primary:hover {
  background-color: #1976d2;
}
.bg-primary-color .btn-outline-primary:hover {
  color: #1976d2;
  background-color: #ffffff;
}

.section > p {
  color: #1976d2;
  text-align: center;
  font-style: italic;
}
.section-dark > p {
  color: #ffffff;
}

@media (max-width: 575px) {
  .rank-demo-view h3 {
    text-align: center;
  }
  .rank-demo-view {
    padding: 0.01rem 0rem;
  }
  .jumbotron {
    padding: 1rem 0rem !important;
  }
  .speaker time {
    visibility: hidden;
  }
  .btn-outline-primary {
    margin-bottom: 20px;
  }
  .bg-primary-color .btn-outline-primary {
    margin-bottom: 20px;
  }
}
</style>
<style>
a.landing-link {
      color: #ffffff !important;
        text-decoration: underline;
}
</style>
