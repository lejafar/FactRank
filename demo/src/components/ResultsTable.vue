<template>
  <b-table :fields="fields" :items="results" :busy="!results" caption-top>
    <!-- A virtual column -->
    <template v-slot:cell(index)="data">
      {{ (page - 1) * limit + (data.index + 1) }}
    </template>

    <!-- extended statement virtual column -->
    <template v-slot:cell(extended_statement)="data">
      <b-alert
        v-if="data.item.match && data.item.match.matched"
        show
        variant="secondary"
        :class="data.item.match.conclusion.toLowerCase()"
      >
        fact-checked:
        <a :href="fix_url(data.item.match.url)" class="alert-link">
          “{{ data.item.match.statement }}”
          <source-icon :source="matchToSource(data.item.match)" />
        </a>
        <span class="float-right">
          <strong>
            {{ data.item.match.conclusion.toLowerCase().replace("_", " ") }}
          </strong>
        </span>
      </b-alert>
      <blockquote class="blockquote">
        <!-- speaker & source information -->
        <footer
          v-if="data.item.speaker || data.item.source"
          class="blockquote-footer"
        >
          <speaker-info
            :source="data.item.source"
            :speaker="data.item.speaker"
          />
          <p v-if="data.item.source" class="info">
            <source-icon :source="data.item.source" />
          </p>
        </footer>

        <!-- statement -->
        <p class="mb-0 statement">
          <span
            v-if="data.item.context && data.item.context.pre_statement"
            class="text-context"
          >
            {{ data.item.context.pre_statement.content }}
          </span>
          <span>
            {{ data.item.content }}
          </span>
          <span
            v-if="data.item.context && data.item.context.post_statement"
            class="text-context"
          >
            {{ data.item.context.post_statement.content }}
          </span>
        </p>

        <!-- feedback -->
        <feedback :result="data.item" :debug="debug" />
      </blockquote>
    </template>

    <!-- loader -->
    <template v-slot:table-busy>
      <div class="loader-container">
        <rotate-loader :color="'#1976d2'"></rotate-loader>
      </div>
    </template>
  </b-table>
</template>

<script>
import moment from "moment";
import RotateLoader from "vue-spinner/src/RotateLoader";
import Feedback from "./Feedback";
import SourceIcon from "./SourceIcon";
import SpeakerInfo from "./SpeakerInfo";

import utilMixin from "@/mixins/utilMixin";

export default {
  name: "ResultsTable",
  props: ["results", "model_version", "debug", "page", "limit"],
  mixins: [utilMixin],
  components: {
    "rotate-loader": RotateLoader,
    feedback: Feedback,
    "source-icon": SourceIcon,
    "speaker-info": SpeakerInfo,
  },
  data() {
    return {
      fields: [
        {
          key: "index",
          label: "#",
        },
        {
          key: "extended_statement",
          label: "Statement",
        },
      ],
    };
  },
  methods: {
    checkworthy(confidence) {
      return confidence > 0.5;
    },
    fix_url(url) {
      if (!url.startsWith("https://")) {
        url = "https://" + url;
      }
      return url;
    },
    matchToSource(match) {
      var source = {};
      if (match.url.includes("knack")) {
        source["type"] = "KNACK_FACTCHECK";
      } else if (match.url.includes("nieuwscheckers")) {
        source["type"] = "NIEUWSCHECKERS";
      } else if (match.url.includes("factcheck")) {
        source["type"] = "FACTCHECK_VLAANDEREN";
      } else {
        source["type"] = "";
      }
      source.url = this.fix_url(match.url);
      return source;
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
p.statement {
  font-size: 1rem;
}

blockquote > footer.blockquote-footer {
  font-size: 70%;
  margin-bottom: 0.3rem;
}

.blockquote {
  margin-bottom: 0rem;
}

footer > p.info {
  float: right;
  min-width: 300px;
  text-align: right;
  margin-bottom: 0;
}

.factchecked svg {
  width: 12px;
}

.factchecked svg.search {
  margin-right: 5px;
}

.factchecked svg.link {
  margin-left: 5px;
}

.text-context {
  color: #b4bbc1;
}

.loader-container {
  text-align: center;
  vertical-align: middle;
  line-height: 300px;
}

tr svg.url {
  /*visibility: hidden;*/
  /*opacity: 0;*/
  visibility: visible;
  opacity: 1;
  transition: visibility 0s 0.5s, opacity 0.5s linear;
  margin-right: -0.5rem;
}

tr:hover svg.url {
  visibility: visible;
  opacity: 1;
  transition: opacity 0.5s linear;
}

.table td {
  padding-bottom: 0.5rem !important;
}

table.b-table[aria-busy="true"] {
  opacity: 1;
}

.alert > a > .link {
  margin-bottom: 3px;
  margin-left: 5px;
}

@media (max-width: 575px) {
  footer > p.info {
    min-width: 200px;
  }
}

.alert-secondary {
  background-color: #f5f5f5 !important;
}

.grotendeels_waar {
  color: #155724 !important;
  background-color: #d4edda !important;
  border-color: #c3e6cb !important;
}

.onwaar {
  color: #721c24 !important;
  background-color: #f8d7da !important;
  border-color: #f5c6cb !important;
}

.onduidelijk {
  color: #856404 !important;
  background-color: #fff3cd !important;
  border-color: #ffeeba !important;
}
</style>
