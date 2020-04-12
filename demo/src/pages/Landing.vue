<template>
  <div>
    <div class="bg-primary-color secondary-color">
    <b-container class="factrank-info">
      <b-jumbotron>
        <vue-markdown class="navbar-brand navbar-subtitle">{{ $t("factranker.content.lead") }}</vue-markdown>
        <ul class="features">
        <li class="yes">FactRank identifies claims in transcripts of parliamentary debates and other Dutch-language texts.</li>
        <li class="yes">FactRank collects feedback about identified check-worthy claims and is periodicaly retrained to self-improve</li>
        <li class="yes">FactRank allows you to search your own source for claims that are factual and check-worthy, by <b-link to="/demo" class="landing-link">enter your own text</b-link> or using our API </li>
        <li class="no">FactRank is <b>not</b> an automatic fact-checker – whether the identified claims are true or false, has to be determined by a fact-check.</li>
        </ul>
      </b-jumbotron>
      <div class="spacing bg-primary-color"/>
    </b-container>
    </div>
    <b-container class="rank-demo-view">
      <h3>Subtitles</h3>
      <ranker :limit="5" source_type="VRT_TERZAKE" :demo="true"/>
    </b-container>
	<div class="bg-primary-color secondary-color">
    <b-container class="rank-demo-view">
      <h3>Parliament</h3>
      <ranker :limit="5" source_type="FLEMISH_PARLIAMENTARY_MEETING" :demo="true"/>
    </b-container>
	</div>
    <b-container class="rank-demo-view">
      <h3>Fact-checks</h3>
      <ranker :limit="5" source_type="KNACK_FACTCHECK" :demo="true"/>
    </b-container>
	<div class="bg-primary-color secondary-color">
    <b-container class="rank-demo-view">
      <h3>Social</h3>
      <ranker :limit="5" source_type="TWITTER" :demo="true"/>
    </b-container>
	</div>
  </div>
</template>

<script>
import Ranker from "@/components/Ranker";

export default {
  name: "FactRanker",
  components: {
    ranker: Ranker,
  }
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
  margin-bottom: 2rem;
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
    margin: .75rem 0rem;
}
li.yes:before, li.no:before{
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
  animation-delay: 1.0s;
}
li:nth-child(3) {
  animation-delay: 1.5s;
}
li:nth-child(4) {
  animation-delay: 2.0s;
}

@keyframes fadeIn {
  0% {
    opacity: 0.0;
  }
  100% {
    opacity: 1.0;
  }
}
.rank-demo-view {
	padding: 2rem 0rem;
}
</style>
