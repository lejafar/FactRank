<template>
    <b-table v-if="result.predictions"
            :fields="fields"
            :items="result.predictions"
            :sort-compare="customSortCompare"
            caption-top>

      <!-- Information about Source of Statements IF meta is set -->
      <template v-if="result.meta" slot="table-caption">
        <p v-if="result.meta.date" >
          Top 50 Check-Whorty Factual statements from
          <span v-if="this.last"> last Plenary Meeting ({{result.meta.date}}, <strong>{{result.meta.amount}}</strong> statements)</span>
          <span v-else> Plenary Meeting on {{result.meta.date}} ({{result.meta.amount}} statements)</span></p>
        <a v-if="result.meta.url.length" :href="result.meta.url"><icon name="link" /> {{result.meta.url}} </a>
      </template>

      <!-- speaker_info_sentence virtual column -->
      <template slot="speaker_info_sentence" slot-scope="data">
        <sentence-extended  v-bind:sentence="data.item"/>
        <!-- <a @click.stop="data.toggleDetails" class="info"><icon name="info-circle" /></a> -->
      </template>

      <template slot="row-details" slot-scope="data">
        <b-card>
          {{data.item.feedback}}
        </b-card>
      </template>
    </b-table>
    <div v-else class="loader-container">
      <rotate-loader :color="'#ffc107'"></rotate-loader>
    </div>
</template>

<script>
import SentenceExtended from '@/components/SentenceExtended'
import RotateLoader from 'vue-spinner/src/RotateLoader'

export default {
  name: 'ResultsTable',
  props: ['result'],
  components: {
    'sentence-extended': SentenceExtended,
    'rotate-loader': RotateLoader
  },
  data () {
    return {
      fields: [
        // A column that needs custom formatting
        { key: 'speaker_info_sentence', label: 'Sentence' },
        // A regular column
        { key: 'probability', sortable: true , label: '<abbr title="Check-Worthyness">CW </abbr>',
          formatter: (value, key, item) => {
            return Number((item.probability[1]*100).toFixed(0)) + ' %'
          } , 'class': 'text-center'}
      ],
      tag: 'last',
      last: true,
    }
  },
  methods: {
    customSortCompare(a, b, key){
      if (typeof a[key][1] === 'number' && typeof b[key][1] === 'number') {
        // If both compared fields are native numbers
        return a[key][1] < b[key][1] ? -1 : (a[key][1] > b[key][1] ? 1 : 0)
      } else {
        // Stringify the field data and use String.localeCompare
        return toString(a[key]).localeCompare(toString(b[key]), undefined, {
          numeric: true
        })
      }
    }
  },
  filters: {
    truncate(number){
      return Number((number*100).toFixed(0)) + ' %';
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
a.info{
  cursor: pointer;
}
blockquote{
  font-size: 1rem;
  margin: 0 0 0rem;
}
abbr{
  margin-right: 35px;
}

.loader-container{
  text-align: center;
  vertical-align: middle;
  line-height: 300px;
}
</style>
