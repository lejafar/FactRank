<template>
  <b-container>
    <b-form-group
      id="fieldset"
      :description="$t('tool.description')"
      :invalid-feedback="invalidFeedback"
      :valid-feedback="validFeedback"
      :state="state"
    >
      <b-form-textarea
        id="input_sentences"
        v-model="sentence_input"
        :placeholder="$t('tool.enter-some-text')"
        :rows="5"
        :max-rows="10"
        @keydown.meta.13="makePrediction(sentence_input)"
      ></b-form-textarea>
    </b-form-group>

    <b-row align-h="between" id="control_line">
      <b-col cols="4">
        <b>{{ sentence_result.category }}</b>
      </b-col>
      <b-col cols="4" class="right-align">
        <b-btn
          variant="outline-primary"
          class="submit_button"
          v-on:click="makePrediction(sentence_input)"
        >
          {{ $t("tool.submit") }}
        </b-btn>
      </b-col>
    </b-row>
    <b-form-group v-if="sentence_result">
      <b-alert show variant="light" class="text-right"></b-alert>
    </b-form-group>
    <b-alert v-if="response_code == 429" show variant="danger">
      {{ $t("tool.429", { max: 200 }) }}
    </b-alert>
    <b-alert v-if="response_code == 500" show variant="danger">
      {{ $t("tool.500") }}
    </b-alert>
    <results-table
      v-else-if="show_result"
      v-bind:results="sentence_result"
      :page="1"
      :limit="1"
    />
  </b-container>
</template>

<script>
import ResultsTable from "../components/ResultsTable";

export default {
  name: "Api",
  props: {
    sentence_input: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      sentence_result: [],
      show_result: false,
      detection: "cfs",
      response_code: 200,
    };
  },
  components: {
    "results-table": ResultsTable,
  },
  computed: {
    state() {
      return this.sentence_input.trim().split(" ").length >= 6 ? true : false;
    },
    invalidFeedback() {
      if (this.sentence_input.trim().split(" ").length >= 6) {
        return "";
      } else if (this.sentence_input.trim().split(" ").length > 0) {
        return this.$t("tool.at-least");
      } else {
        return this.$t("tool.enter-something");
      }
    },
    validFeedback() {
      return this.state === true ? this.$t("tool.thanks") : "";
    },
  },
  methods: {
    makePrediction(sentences) {
      this.sentence_result = false;
      this.show_result = true;
      if (![".", "?", "!"].includes(sentences.trim().slice(-1))) {
        sentences = sentences + ".";
        this.sentence_input = sentences;
      }
      var req = {
        detect: this.detection,
        text: sentences,
      };
      fetch("https://api-v2.factrank.org/", {
        body: JSON.stringify(req),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          this.response_code = response.status;
          return response.json();
        })
        .then((data) => {
          this.sentence_result = data;
        });
    },
  },
  mounted() {
    if (this.sentence_input != "") {
      this.makePrediction(this.sentence_input);
    }
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#input_sentences {
  margin-bottom: 1rem;
}

.right-align {
  text-align: right;
}

.submit_button {
  margin-top: -70px;
}

.form-group {
  margin-bottom: 0rem;
}

/*  Change submit button margin in sync with bootstrap breakpoints */
@media (max-width: 768px) {
  .submit_button {
    margin-top: 0px;
  }

  .form-group {
    margin-bottom: 1rem;
  }
}
</style>
