<template>
    <b-table
        v-if="results"
        :fields="fields"
        :items="results"
        caption-top>

        <!-- A virtual column -->
        <template slot="index" slot-scope="data">
            {{ data.index + 1 }}
        </template>

        <!-- extended statement virtual column -->
        <template slot="extended_statement" slot-scope="data">
            <blockquote class="blockquote">
                <footer class="blockquote-footer">
                    <span class="speaker">
                        {{data.item.speaker.name}}
                        <cite v-if="data.item.speaker && data.item.speaker.association" title="Speaker">({{data.item.speaker.association.name}})</cite>
                    </span>
                    <p v-if="data.item.source" class="info">
                        <span v-if="pureDate(data.item.source.published_at)">
                            {{ data.item.source.published_at + '+00' | moment('timezone', 'Europe/Brussels') | moment("MMM Do YYYY")}}
                        </span>
                        <span v-else>
                            {{ data.item.source.published_at + '+00' | moment('timezone', 'Europe/Brussels') | moment("MMM Do YYYY H:mm")}}
                        </span>
                        <a class="source_type text-secondary" :href="data.item.source.url" target="_blank">
                            <icon :class="data.item.source.type.toLowerCase()" :name="data.item.source.type | pick_icon" size="xs"/>
                        </a>
                    </p>
                </footer>
                <p class="mb-0 statement">
                    <span v-if="data.item.context && data.item.context.pre_statement" class="text-context">
                        {{data.item.context.pre_statement.content}}
                    </span>
                    <span>
                        {{data.item.content}}
                    </span>
                    <span v-if="data.item.context && data.item.context.post_statement" class="text-context">
                        {{data.item.context.post_statement.content}}
                    </span>
                    <p class="text-secondary confidence">
                        check-worthiness: {{data.item.predictions[0].confidence | truncate}}
                    </p>
                </p>
            </blockquote>
        </template>

    </b-table>
    <div v-else class="loader-container">
        <rotate-loader :color="'#ffc107'"></rotate-loader>
    </div>
</template>

<script>
import RotateLoader from 'vue-spinner/src/RotateLoader'

export default {
    name: 'ResultsTable',
    props: ['results'],
    components: {
        'rotate-loader': RotateLoader
    },
    data () {
        return {
            fields: [
                { key: 'index', label: '#'},
                { key: 'extended_statement', label: 'Statement'},
            ],
        }
    },
    methods: {
        pureDate(time_stamp) {
            let [date, time] = time_stamp.split(' ');
            let [hour, minute, second] = time.split(':');
            return (hour === '00' && minute === '00')
        }
    },
    filters: {
        pre_date(time_stamp) {
            let [date, time] = time_stamp.split(' ');
            let [hour, minute, second] = time.split(':');
            if (hour != '00' || minute != '00'){
                // make sure this is recognized as UTC timestamp
                return time_stamp + '+00';
            }
            return date;
        },
        pick_icon(source_type) {
            if(source_type == 'TWITTER'){
                return 'brands/twitter';
            }
            return 'university';
        },
        truncate(number){
            return Number((number*100).toFixed(0)) + ' %';
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
p.statement {
    font-size: 1rem;
}
blockquote > footer.blockquote-footer {
    font-size: 70%;
    margin-bottom: .3rem;
}
footer > p.info {
    float: right;
}
.source_type > svg {
    margin-left: .5rem;
}
.text-context {
    color: #b4bbc1;
}
svg.twitter {
    color: #1da1f2;
}
p.confidence {
    float: right;
    margin-bottom: 0rem;
    font-size: 50%;
    font-style: italic;
}
.loader-container{
  text-align: center;
  vertical-align: middle;
  line-height: 300px;
}
</style>
