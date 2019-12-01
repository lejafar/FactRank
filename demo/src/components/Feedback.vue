<template>
	<span class="feedback">
		<p v-if="debug" class="text-secondary confidence bottom">
        <span> (confidence: {{result.confidence | round}}, score: {{result.score | round}}) </span>
		</p>
		<p class="text-secondary confidence bottom">
			<span v-if="metric > 0.99"> 🔥 Check-Worthy</span>
			<span v-else-if="metric > 0.85"> ✔︎ Check-Worthy</span>
			<span v-else-if="metric > 0.50"> Might be Check-Worthy (confidence: {{metric | truncate}}) </span>
		</p>
        <template v-if="feedbackAvailable()">
            <p v-if="!$auth.loading && $auth.isAuthenticated && fetchFeedback($auth.user)" class="text-secondary feedback">
                <b-spinner v-if="not_yet_fetched_feedback" :variant="warning" :key="warning" type="grow"></b-spinner>
                <span v-else-if="user_feedback">
                    <span v-if="user_feedback == 'FR'">
                        <b-button pill variant="success" @click="postAgreement($auth.user)" >{{update(result.upvotes, 'FR')}}<icon class="feedback" name="thumbs-up" scale="1"/></b-button>
                        <b-button pill variant="outline-danger" @click="postDisagreement($auth.user)" >{{update(result.downvotes, 'NFR')}}<icon class="feedback" name="thumbs-down" scale="1"/></b-button>
                    </span>
                    <span v-else>
                        <b-button pill variant="outline-success" @click="postAgreement($auth.user)" >{{update(result.upvotes, 'FR')}}<icon class="feedback" name="thumbs-up" scale="1"/></b-button>
                        <b-button pill variant="danger" @click="postDisagreement($auth.user)" >{{update(result.downvotes, 'NFR')}}<icon class="feedback" name="thumbs-down" scale="1"/></b-button>
                    </span>
                </span>
                <span v-else>
                    <b-button pill variant="outline-success" @click="postAgreement($auth.user)" >{{update(result.upvotes, 'FR')}}<icon class="feedback" name="thumbs-up" scale="1"/></b-button>
                    <b-button pill variant="outline-danger" @click="postDisagreement($auth.user)" >{{update(result.downvotes, 'NFR')}}<icon class="feedback" name="thumbs-down" scale="1"/></b-button>
                </span>
            </p>
            <p v-else class="text-secondary feedback feedback-results">
            <b-button pill @click="login" variant="outline-success" class="vote-result">{{update(result.upvotes, 'FR')}}<icon class="feedback" name="thumbs-up" scale="1"/></b-button>
                <b-button pill @click="login" variant="outline-danger" class="vote-result">{{update(result.downvotes, 'NFR')}}<icon class="feedback" name="thumbs-down" scale="1"/></b-button>
            </p>
        </template>
	</span>
</template>

<script>
export default {
    name: 'Feedback',
    props: {
        result: Object,
        debug: Boolean,
    },
    data () {
        return {
			user_feedback: '',
			not_yet_fetched_feedback: true,
            metric: this.result.score || this.result.confidence
        }
    },
	methods: {
        feedbackAvailable() {
            return ('id' in this.result);
        },
		// Log the user in
		login() {
			this.$auth.loginWithPopup();
		},
        postFeedback (user, expected_label=null) {
			var body = {'user': user, 'prediction_id': this.result['predictions.id']};
			if(expected_label != null){
				body['expected_label']= expected_label;
			}
            fetch("https://api-v2.factrank.org/feedback", {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(body),
            }).then(response => response.json()).then((data) => {
				this.user_feedback = 'expected_label' in data ? data['expected_label'] : '';
				this.not_yet_fetched_feedback = false;
            });
		},
		postAgreement(user) {
            const was_up = this.user_feedback == 'FR';
            const was_down = this.user_feedback == 'NFR';
			this.postFeedback(user, this.user_feedback == 'FR' ? '' : 'FR');
            const is_up = this.user_feedback == 'FR';
            if(!was_up && is_up) this.upvotes += 1;
            if(was_down && is_up){
                this.downvotes -= 1;
                this.upvotes += 1;
            }
            if(!was_down && is_up){
                this.upvotes += 1;
            }
		},
		postDisagreement(user) {
			this.postFeedback(user, this.user_feedback == 'NFR' ? '' : 'NFR');
            this.downvotes += 1;
		},
		fetchFeedback(user) {
			this.postFeedback(user);
			return true;
		},
        update(votes, label) {
            return votes + (this.user_feedback == label ? 1 : 0);
        }

	},
	filters: {
        round(number){
            return parseFloat(Math.round(number * 100) / 100).toFixed(2);
        },
        truncate(number){
            return Number((number*100).toFixed(0)) + ' %';
        },
	},
    mounted() {
        this.upvotes = this.result.upvotes;
        this.downvotes = this.result.downvotes;
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
p.bottom {
	display: inline-block;
    margin-bottom: 0rem;
    font-size: 50%;
    font-style: italic;
    margin-top: .5rem;
    margin-right: .5rem;
	margin-left: .5rem;
}
span.feedback {
    float: right;
}
p.feedback, p.feedback-results {
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
.btn-sm, .btn-group-sm > .btn {
    padding: 0.15rem 0.3rem;
    font-size: 0.65rem;
}
.btn-outline-secondary {
	border: 0;
    border-style: dotted;
}
.votes {
    line-height: .8;
    padding: 0.8em;
    border-radius: 20rem;
    background: #b4bbc1;
}
</style>
