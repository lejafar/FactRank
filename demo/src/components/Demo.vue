<template>
  <div>
    <b-form-group
      id="fieldset"
      description="Try one or more staments and see whether they appear Check-Whorty to FactRank"
      :invalid-feedback="invalidFeedback"
      :valid-feedback="validFeedback"
      :state="state"
    >
        <b-form-textarea id="input_sentences"
                         v-model="input"
                         placeholder="Enter some text ..."
                         :rows="10"
                         :max-rows="20"
                         @keydown.meta.13="postPredictionJob()">
        </b-form-textarea>
      </b-form-group>

      <b-row align-h="between" id="control_line">
        <b-col cols="12" class="right-align">
          <b-btn variant="outline-primary" class="submit_button"  v-on:click="postPredictionJob()">submit</b-btn>
        </b-col>
      </b-row>
      <b-form-group v-if="result" >
        <b-alert show variant="light" class="text-right">
        </b-alert>
     </b-form-group>
      <b-progress v-if="processing()" :value="progress" :max="110" animated></b-progress>
      <results-table v-if="!processing()" hide-loader v-bind:results="result" :debug="debug"/>
  </div>
</template>

<script>
import ResultsTable from '@/components/ResultsTable'

export default {
  name: 'Demo',
  data () {
    return {
      id: null,
      input: '',
      progress: null,
      result: null,
      debug: false,
      prediction_endpoint: `${this.$api_url}/jobs/inference/${this.$model_suffix}`,
      poller: null
    }
  },
  components: {
    'results-table': ResultsTable
  },
  computed: {
   state () {
     return this.input.trim().split(' ').length >= 6 ? true : false
   },
   invalidFeedback () {
     if (this.input.trim().split(' ').length >= 6) {
       return ''
     } else if (this.input.trim().split(' ').length > 0) {
       return 'Enter at least 6 words'
     } else {
       return 'Please enter something'
     }
   },
   validFeedback () {
     return this.state === true ? 'Thank you' : ''
   }
 },
  methods: {
   processing() {
       return this.progress != null && this.result == null;
   },
    set_progress(value) {
        if(this.id != null){
            // if id is assigned, progress is set to 10
            value += 10;
        }
        this.progress = value;
    },
    fetchPredictionProgress() {
        fetch(`${this.prediction_endpoint}/${this.id}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
        }).then(response => response.json()).then((data) => {
            // if `id` is not returned, it is invalid
            if(!('id' in data)) return;
            this.set_progress(data.progress);
            if('result' in data){
                this.result = data.result;
                this.progress = null
            }
        });
    },
    postPredictionJob () {
      // reset
      this.id = null;
      this.progress = 0;
      this.result = null;
      // post job
      fetch(this.prediction_endpoint, {
          body: JSON.stringify({'text': this.input}),
          method: "POST",
          headers: {
            "Content-Type": "application/json",
        },
      }).then(response => response.json())
        .then((data) => {
          this.id = data.id;
          this.set_progress(0);
        })
    }
  },
  mounted() {
    this.debug = this.$route.query.debug || false
    this.poller = setInterval(function () {
        if(this.id != null && this.result == null){
            this.fetchPredictionProgress();
        }
      }.bind(this), 100);
  },
    beforeDestroy () {
        clearInterval(this.poller);
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#input_sentences {
  margin-bottom: 1rem;
}
.right-align{
  text-align: right;
}
.submit_button{
    margin-top: -70px;
}
.form-group{
  margin-bottom: 0rem;
}

/*  Change submit button margin in sync with bootstrap breakpoints */
@media (max-width: 768px) {
  .submit_button{
      margin-top: 0px;
  }
  .form-group{
    margin-bottom: 1rem;
  }

}
</style>
