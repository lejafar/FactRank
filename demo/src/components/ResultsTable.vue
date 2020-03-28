<template>
    <b-table
        :fields="fields"
        :items="results"
        :busy="!results"
        caption-top>

        <!-- A virtual column -->
        <template v-slot:cell(index)="data">
            {{ (page - 1) * limit + (data.index + 1) }}
        </template>

        <!-- extended statement virtual column -->
        <template v-slot:cell(extended_statement)="data">
            <blockquote class="blockquote">
                <footer v-if="data.item.speaker || data.item.source "class="blockquote-footer">
                    <span v-if="data.item.speaker" class="speaker">
                        {{data.item.speaker.country | flag(data.item.source.name) }}
                        {{data.item.speaker.name | cleanName }}
                        <cite v-if="data.item.speaker && data.item.speaker.association" title="Speaker">({{data.item.speaker.association.name}})</cite>
                    </span>
                    <span v-else-if="data.item.source.is_factcheck == 1" class="speaker factchecked">
                        <a class="source_type text-secondary" :href="data.item.source.url" target="_blank">
							<b-badge pill variant="primary"><icon class="search" name="search" scale="1"/>FactCheck Available<icon name="link" class="link" size="xs"/></b-badge>
						</a>
                    </span>
                    <span v-else class="speaker">
                        <b>{{data.item.source.name.split("2")[0]}}</b> {{data.item.source.published_at | formatDate(true)}}
                    </span>
                    <p v-if="data.item.source" class="info">
                        {{ data.item.source.published_at | formatDate }}
                        <a class="source_type text-secondary" :href="data.item.source.url" target="_blank">
							<template v-if="data.item.source.type == 'FACTCHECK_VLAANDEREN'">
								<img style="vertical-align:middle;max-height: 15px;" src="https://factcheck.vlaanderen/static/favicon/favicon-32x32.png">
							</template>
							<template v-else-if="data.item.source.type.startsWith('VRT')">
								<svg class="vrt_logo" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300.37 76.02" focusable="false">
									<title>VRT NWS</title>
									<path d="M37,75.94a37,37,0,1,1,0-74H74v37a37,37,0,0,1-37,37" fill="#5dfc71"></path>
									<path d="M284.7,22.25a1,1,0,0,1-1-.93c-.72-6.19-6.73-9.56-15.45-9.56-7.09,0-13.88,2.67-13.88,8.74,0,18.61,46-2.16,46,32.9,0,0,0,22.62-31.46,22.62-28.14,0-30.35-18.43-30.6-24.46a1,1,0,0,1,1-1h13a1,1,0,0,1,1,1c.75,10,8.73,12.72,16.6,12.72s15.63-3,15.63-10.49c0-19-46.05.93-46.05-32.79,0-10.28,9.66-21,29.81-21,19.36,0,28.64,9.68,29.27,21.25a1,1,0,0,1-.94,1.06h-.06Z" fill="#16284a"></path>
									<path d="M55.71,49a7.14,7.14,0,0,0,7.11-7.17h0q0-.08,0-.15v-.1a.45.45,0,0,0-.46-.44H58.77a.65.65,0,0,0-.67.63h0a2.33,2.33,0,0,1-2.23,2.43h-.08c-1.37,0-2.32-1-2.32-2.72V33.56h6.4a.45.45,0,0,0,.45-.45h0v-3.4a.45.45,0,0,0-.45-.45h-6.4V24.39a.45.45,0,0,0-.45-.45H48.85a.46.46,0,0,0-.46.46V41.17c0,4.7,3,7.85,7.31,7.85" fill="#16284a"></path>
									<path d="M38.29,46.94v-6.4c.14-4,2.9-7.15,6.86-7h.2a.5.5,0,0,0,.52-.48h0V29.63a.5.5,0,0,0-.47-.5c-2.47-.17-5.16.19-7.3,2.81V29.76a.5.5,0,0,0-.49-.51H33.73a.5.5,0,0,0-.5.5h0V48.22a.5.5,0,0,0,.5.5h4.06a.5.5,0,0,0,.5-.5Z" fill="#16284a"></path>
									<path d="M30.19,29.26H26a.5.5,0,0,0-.48.36l-4,12.72h-.08L17.33,29.62a.51.51,0,0,0-.48-.36H12.6a.5.5,0,0,0-.48.66l6.35,18.46a.5.5,0,0,0,.48.35h4.88a.5.5,0,0,0,.48-.35l6.36-18.44a.51.51,0,0,0-.34-.64h-.14" fill="#16284a"></path>
									<path d="M239.74,2h-12.1a1,1,0,0,0-1,.79l-12,54.61-11-54.6a1,1,0,0,0-1-.81H184.89a1,1,0,0,0-1,.81l-11,54.6L160.8,2.78a1,1,0,0,0-1-.79H147.72a1,1,0,0,0-1,1.24l16.59,70a1,1,0,0,0,1,.77h17.3a1,1,0,0,0,1-.8l11.14-54.4,11.14,54.4a1,1,0,0,0,1,.8h17.3a1,1,0,0,0,1-.77l16.53-70A1,1,0,0,0,240,2h-.28Z" fill="#16284a"></path>
									<path d="M97.92,23.38h-.2V72.94a1,1,0,0,1-1,1H84.84a1,1,0,0,1-1-1V3a1,1,0,0,1,1-1h15.78a1,1,0,0,1,.87.51l28.19,49.35h.2V3a1,1,0,0,1,1-1h11.87a1,1,0,0,1,1,1V72.94a1,1,0,0,1-1,1H127.24a1,1,0,0,1-.88-.51Z" fill="#16284a"></path>
								</svg>
							</template>
							<template v-else-if="data.item.source.type.startsWith('NIEUWSCHECKERS')">
                            <svg class="nc_logo">
                                <circle xmlns="http://www.w3.org/2000/svg" class="st0b" cx="5" cy="5" r="5"></circle>
                            </svg>
							</template>
							<template v-else>
								<img v-if="flemish(data.item.source.name)" style="vertical-align:middle;max-height: 15px;" src="https://www.vlaamsparlement.be/sites/all/themes/balance_theme/favicon.ico">
								<icon :class="data.item.source.type.toLowerCase()" :name="data.item.source.type | pick_icon" size="xs"/>
							</template>
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
                </p>
                <feedback :result="data.item" :debug="debug"/>
            </blockquote>
        </template>
        <template v-slot:table-busy>
            <div class="loader-container">
            <rotate-loader :color="'#ffc107'"></rotate-loader>
            </div>
        </template>
    </b-table>
</template>

<script>
import moment from 'moment'
import RotateLoader from 'vue-spinner/src/RotateLoader'
import Feedback from './Feedback'

export default {
    name: 'ResultsTable',
    props: ['results', 'model_version', 'debug', 'page', 'limit'],
    components: {
        'rotate-loader': RotateLoader,
        'feedback': Feedback
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
        checkworthy(confidence) {
            return confidence > .5;
        }
    },
    filters: {
        cleanName(name) {
            return name.replace("De heer", "").replace("Mevrouw", "").replace("Minister", "")
        },
        formatDate(time_stamp, short=false) {
            // make sure this is recognized as UTC timestamp
            time_stamp += '+00'
            var published_at = moment(time_stamp);
            // determine format string
            var year_format_str = "YYYY";
            var time_format_str = ""
            let [date, time] = time_stamp.split(' ');
            let [hour, minute, second] = time.split(':');
            if (hour != '00' || minute != '00'){
                time_format_str = " H:mm";
            }
            if (short) {
                return published_at.calendar(null, { lastWeek: `LL`, sameElse: `LL`});
            } else {
                return published_at.calendar(null, { sameElse: `LLL`});
            }
        },
        pick_icon(source_type) {
            if(source_type == 'TWITTER'){
                return 'brands/twitter';
            }
            return 'university';
        },
        flag(country, source) {
            if(country == 'BE'){
                return '🇧🇪 ';
            }
            return '🇳🇱 ';
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
	min-width: 300px;
    text-align: right;
    margin-bottom: 0;
}
.source_type > svg {
    margin-left: .5rem;
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
svg.twitter {
    color: #1da1f2;
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
.vrt_logo {
    max-width: 50px;
}
.nc_logo {
    height: 10px;
    max-width: 10px;
    margin-bottom: 5px;
}
.st0b{fill:#6BBA0F;}
.st1b{fill:#0D3875;}
table.b-table[aria-busy='true'] {
  opacity: 1.0;
}
</style>
