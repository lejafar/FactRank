<template>
  <span class="feedback">
    <p v-if="debug" class="text-secondary confidence bottom">
      <span>(score: {{ result.score | round }})</span>
    </p>
    <p class="text-secondary confidence bottom">
      <span
        v-if="result.score > 0.99"
        v-b-tooltip.hover
        :title="`AI-confidence: ${truncate(result.score)}`"
      >
        🔥 Check-Worthy
      </span>
      <span
        v-else-if="result.score > 0.85"
        v-b-tooltip.hover
        :title="`AI-confidence: ${truncate(result.score)}`"
      >
        ✔︎ Check-Worthy
      </span>
      <span
        v-else-if="result.score > 0.5"
        v-b-tooltip.hover
        :title="`AI-confidence: ${truncate(result.score)}`"
      >
        Might be Check-Worthy
      </span>
      <span
        v-else
        v-b-tooltip.hover
        :title="`AI-confidence: ${truncate(result.score)}`"
      >
        ✘ Not Check-Worthy
      </span>
    </p>
    <template v-if="doesHaveVotes">
      <p
        v-if="
          !$auth.loading &&
          $auth.isAuthenticated &&
          $auth.user &&
          fetchFeedback($auth.user)
        "
        class="text-secondary feedback"
      >
        <b-spinner
          v-if="not_yet_fetched_feedback"
          variant="warning"
          key="warning"
          type="grow"
        ></b-spinner>
        <span v-else-if="user_feedback">
          <span v-if="user_feedback == 'FR'">
            <b-button
              pill
              v-b-tooltip.hover
              :title="$t('factranker.feedback.positive')"
              @click="postAgreement($auth.user)"
              variant="success"
              class="vote-result"
            >
              {{ this.upvotes }}
              <icon class="feedback" name="search" scale="1" />
            </b-button>
            <b-button
              pill
              v-b-tooltip.hover
              :title="$t('factranker.feedback.negative')"
              @click="postDisagreement($auth.user)"
              variant="outline-danger"
              class="vote-result"
            >
              {{ this.downvotes }}
              <icon class="feedback" name="trash" scale="1" />
            </b-button>
          </span>
          <span v-else>
            <b-button
              pill
              v-b-tooltip.hover
              :title="$t('factranker.feedback.positive')"
              @click="postAgreement($auth.user)"
              variant="outline-success"
              class="vote-result"
            >
              {{ this.upvotes }}
              <icon class="feedback" name="search" scale="1" />
            </b-button>
            <b-button
              pill
              v-b-tooltip.hover
              :title="$t('factranker.feedback.negative')"
              @click="postDisagreement($auth.user)"
              variant="danger"
              class="vote-result"
            >
              {{ this.downvotes }}
              <icon class="feedback" name="trash" scale="1" />
            </b-button>
          </span>
        </span>
        <span v-else>
          <b-button
            pill
            v-b-tooltip.hover
            :title="$t('factranker.feedback.positive')"
            @click="postAgreement($auth.user)"
            variant="outline-success"
            class="vote-result"
          >
            {{ this.upvotes }}
            <icon class="feedback" name="search" scale="1" />
          </b-button>
          <b-button
            pill
            v-b-tooltip.hover
            :title="$t('factranker.feedback.negative')"
            @click="postDisagreement($auth.user)"
            variant="outline-danger"
            class="vote-result"
          >
            {{ this.downvotes }}
            <icon class="feedback" name="trash" scale="1" />
          </b-button>
        </span>
      </p>
      <p v-else class="text-secondary feedback feedback-results">
        <b-button
          pill
          v-b-tooltip.hover
          :title="$t('factranker.feedback.positive')"
          @click="login"
          variant="outline-success"
          class="vote-result"
        >
          {{ this.upvotes }}
          <icon class="feedback" name="search" scale="1" />
        </b-button>
        <b-button
          pill
          v-b-tooltip.hover
          :title="$t('factranker.feedback.negative')"
          @click="login"
          variant="outline-danger"
          class="vote-result"
        >
          {{ this.downvotes }}
          <icon class="feedback" name="trash" scale="1" />
        </b-button>
      </p>
    </template>
  </span>
</template>

<script>
export default {
  name: "Feedback",
  props: ["result", "debug"],
  data() {
    return {
      user_feedback: "",
      upvotes: 0,
      downvotes: 0,
      not_yet_fetched_feedback: true,
    };
  },
  computed: {
    // a computed getter
    doesHaveVotes: function () {
      // `this` points to the vm instance
      return ("upvotes" in this.result) | ("downvotes" in this.result);
    },
  },
  methods: {
    // Log the user in
    login() {
      this.$auth.loginWithPopup();
    },
    postFeedback(user, expected_label = null) {
      var body = {
        user: user,
        prediction_id: this.result["predictions.id"],
      };
      if (expected_label != null) {
        body["expected_label"] = expected_label;
      }
      fetch("https://api-v2.factrank.org/feedback", {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      })
        .then((response) => response.json())
        .then((data) => {
          this.user_feedback =
            "expected_label" in data ? data["expected_label"] : "";
          this.upvotes =
            "fr_count" in data ? data["fr_count"] : this.result.upvotes;
          this.downvotes =
            "nfr_count" in data ? data["nfr_count"] : this.result.downvotes;
          this.not_yet_fetched_feedback = false;
        });
    },
    postAgreement(user) {
      this.postFeedback(user, this.user_feedback == "FR" ? "" : "FR");
    },
    postDisagreement(user) {
      this.postFeedback(user, this.user_feedback == "NFR" ? "" : "NFR");
    },
    fetchFeedback(user) {
      this.postFeedback(user);
      return true;
    },
    round(number) {
      return parseFloat(Math.round(number * 100) / 100).toFixed(2);
    },
    truncate(number) {
      return Number((number * 100).toFixed(0)) + " %";
    },
  },
  filters: {
    round(number) {
      return parseFloat(Math.round(number * 100) / 100).toFixed(2);
    },
    truncate(number) {
      return Number((number * 100).toFixed(0)) + " %";
    },
  },
  mounted() {
    this.upvotes = this.result.upvotes;
    this.downvotes = this.result.downvotes;
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
p.bottom {
  display: inline-block;
  margin-bottom: 0rem;
  font-size: 50%;
  /*font-style: italic;*/
  margin-top: 0.5rem;
  margin-right: 0.5rem;
  margin-left: 0.5rem;
}

@media (min-width: 576px) {
  span.feedback {
    float: right;
  }
}

p.feedback,
p.feedback-results {
  float: right;
  margin-bottom: 0;
}

.feedback-results > button {
  color: #b4bbc1;
  border-color: #b4bbc1;
}

.feedback-results > button:hover {
  color: #fff;
}

.feedback-results > button.btn-outline-danger:hover {
  border-color: #dc3545;
}

.feedback-results > button.btn-outline-success:hover {
  border-color: #28a745;
}

.feedback button > svg {
  margin-left: 0.4em;
}

.feedback button.btn-outline-success > svg {
  margin-bottom: 0.2em;
}

.btn {
  margin-left: 0.5rem;
  font-size: 55%;
  padding: 0.2em 0.5em;
  border-radius: 50rem !important;
}

svg.feedback.fa-icon {
  width: auto;
  height: 1em;
}

.btn-sm,
.btn-group-sm > .btn {
  padding: 0.15rem 0.3rem;
  font-size: 0.65rem;
}

.btn-outline-secondary {
  border: 0;
  border-style: dotted;
}

.votes {
  line-height: 0.8;
  padding: 0.8em;
  border-radius: 20rem;
  background: #b4bbc1;
}
</style>
