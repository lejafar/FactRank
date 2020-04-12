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
        variant="primary"
      >
        matched to factcheck
        <a :href="data.item.match.url" class="alert-link">
          “{{ data.item.match.statement }}”
          <icon name="link" class="link" size="xs" />
        </a>
        <span class="float-right">
          conclusion was
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
          <source-icon :source="data.item.source" />
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
  visibility: hidden;
  opacity: 0;
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
</style>
