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
                <footer v-if="data.item.speaker || data.item.source "class="blockquote-footer">
                    <span v-if="data.item.speaker" class="speaker">
                        <img v-if="flemish(data.item.source.name)" style="vertical-align:middle;max-height: 15px;" src="https://www.vlaamsparlement.be/sites/all/themes/balance_theme/favicon.ico">
                        {{data.item.speaker.country | flag(data.item.source.name) }}
                        {{data.item.speaker.name}}
                        <cite v-if="data.item.speaker && data.item.speaker.association" title="Speaker">({{data.item.speaker.association.name}})</cite>
                    </span>
                    <p v-if="data.item.source" class="info">
                        {{ data.item.source.published_at | formatDate }}
                        <a class="source_type text-secondary" :href="data.item.source.url" target="_blank">
                            <icon :class="data.item.source.type.toLowerCase()" :name="data.item.source.type | pick_icon" size="xs"/>
                            <icon class="url text-context" name="link" size="xs"/>
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
                        check-worthiness: {{data.item.confidence | truncate}}
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
import moment from 'moment'
import RotateLoader from 'vue-spinner/src/RotateLoader'

export default {
    name: 'ResultsTable',
    props: ['results', 'model_version'],
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
        flemish(source) {
            return source.includes('Flemish');
        },
        checkworthy(condidence) {
            return confidence > .5;
        }
    },
    filters: {
        formatDate(time_stamp) {
            // make sure this is recognized as UTC timestamp
            time_stamp += '+00'
            var published_at = moment(time_stamp);
            // determine format string
            var time_format_str = ""
            let [date, time] = time_stamp.split(' ');
            let [hour, minute, second] = time.split(':');
            if (hour != '00' || minute != '00'){
                time_format_str = " H:mm"
            }
            return published_at.calendar(null, {
                sameDay: `[Today]${time_format_str}`,
                lastDay: `[Yesterday]${time_format_str}`,
                lastWeek: `MMM Do YYYY${time_format_str}`,
                sameElse: `MMM Do YYYY${time_format_str}`
            });
        },
        pick_icon(source_type) {
            if(source_type == 'TWITTER'){
                return 'brands/twitter';
            }
            return 'university';
        },
        flag(country, source) {
            if(country == 'BE'){
                if(source.includes('Flemish')) return;
                return '🇧🇪 ';
            }
            return '🇳🇱 ';
        },
        truncate(number){
            return Number((number*100).toFixed(0)) + ' %';
        },
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
    margin-top: .5rem;
    margin-right: .5rem;
}
.loader-container{
  text-align: center;
  vertical-align: middle;
  line-height: 300px;
}
tr svg.url {
    visibility: hidden;
    opacity: 0;
    transition: visibility 0s 0.5s, opacity 0.5s linear;
    margin-right: -.5rem;
}
tr:hover svg.url {
    visibility: visible;
    opacity: 1;
    transition: opacity 0.5s linear;
}
.table td{
    padding-bottom: .5rem !important;
}
</style>
