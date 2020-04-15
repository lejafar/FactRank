<template>
  <div>
    <div class="bg-primary-color secondary-color">
      <b-container class="factrank-info">
        <b-jumbotron>
          <h3>
            <vue-markdown class="navbar-subtitle">
              {{ $t("factranker.content.lead") }}
            </vue-markdown>
          </h3>
          <ul class="features">
            <li class="yes">
              FactRank identifies claims in transcripts of parliamentary debates
              and other Dutch-language texts.
            </li>
            <li class="yes">
              FactRank collects feedback about identified check-worthy claims
              and is periodicaly retrained to self-improve
            </li>
            <li class="yes">
              FactRank allows you to search your own source for claims that are
              factual and check-worthy, by
              <b-link to="/api" class="landing-link">
                enter your own text
              </b-link>
              or using our API
            </li>
            <li class="no">
              FactRank is
              <b>not</b>
              an automatic fact-checker – whether the identified claims are true
              or false, has to be determined by a fact-check.
            </li>
          </ul>
        </b-jumbotron>
        <div class="spacing bg-primary-color" />
      </b-container>
    </div>
    <div class="bg-tertiary-color secondary-color">
      <b-container class="rank-demo-view">
        <h2>Claim Spotting.</h2>
      </b-container>
    </div>
    <b-container class="rank-demo-view">
      <h3 id="subtitles">Subtitles</h3>
      <ranker :limit="5" source_type="VRT_TERZAKE" :demo="true" />
    </b-container>
    <div class="bg-primary-color secondary-color">
      <b-container class="rank-demo-view">
        <h3>Parliament</h3>
        <ranker
          :limit="5"
          source_type="FLEMISH_PARLIAMENTARY_MEETING"
          :demo="true"
        />
      </b-container>
    </div>
    <b-container class="rank-demo-view">
      <h3>Social</h3>
      <ranker :limit="5" source_type="TWITTER" :demo="true" />
    </b-container>
    <div class="bg-primary-color secondary-color">
      <b-container class="rank-demo-view">
        <h2>Claim Matching.</h2>
      </b-container>
    </div>
    <div class="spacing" />
    <api
      sentence_input="Een arm kind heeft 7 maal meer kans op een C-attest dan gemiddeld.
Belgische vrouwen leveren 56 procent onbetaald werk.
Aan een verslaving aan alcohol sterven meer mensen dan aan tabak."
    />
  </div>
</template>

<script>
import Ranker from "@/components/Ranker";
import Api from "@/pages/Api";

export default {
  name: "FactRanker",
  components: {
    ranker: Ranker,
    api: Api,
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
a.landing-link {
  color: #ffffff !important;
  text-decoration: underline;
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
}
</style>
