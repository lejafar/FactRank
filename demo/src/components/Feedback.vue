<template>
	<span class="feedback">
		<p class="text-secondary confidence bottom">
			<span v-if="result.confidence > 0.99"> 🔥 Check-Worthy</span>
			<span v-else-if="result.confidence > 0.85"> ✔︎ Check-Worthy</span>
			<span v-else-if="result.confidence > 0.5"> Might be Check-Worthy (confidence: {{result.confidence | truncate}}) </span>
		</p>
		<p v-if="!$auth.loading && $auth.isAuthenticated && fetchFeedback($auth.user)" class="text-secondary feedback">
			<b-spinner v-if="not_yet_fetched_feedback" :variant="warning" :key="warning" type="grow"></b-spinner>
			<span v-else-if="user_feedback">
				<span v-if="user_feedback == 'FR'">
					<b-button pill variant="success" @click="postAgreement($auth.user)" >agree</b-button>
					<b-button pill variant="outline-danger" @click="postDisagreement($auth.user)" >disagree</b-button>
				</span>
				<span v-else>
					<b-button pill variant="outline-success" @click="postAgreement($auth.user)" >agree</b-button>
					<b-button pill variant="danger" @click="postDisagreement($auth.user)" >disagree</b-button>
				</span>
			</span>
			<span v-else>
				<b-button pill variant="outline-success" @click="postAgreement($auth.user)" >agree</b-button>
				<b-button pill variant="outline-danger" @click="postDisagreement($auth.user)" >disagree</b-button>
			</span>
		</p>
		<p v-else class="text-secondary give-feedback bottom">
			<b-button variant="outline-secondary" size="sm" @click="login">
				<icon class="feedback" name="pen" scale="1"/> Wrong?
			</b-button>
        </p>
	</span>
</template>

<script>
export default {
    name: 'Feedback',
    props: ['result'],
    data () {
        return {
			user_feedback: '',
			not_yet_fetched_feedback: true,
        }
    },
	methods: {
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
			this.postFeedback(user, this.user_feedback == 'FR' ? '' : 'FR');
		},
		postDisagreement(user) {
			this.postFeedback(user, this.user_feedback == 'NFR' ? '' : 'NFR');
		},
		fetchFeedback(user) {
			this.postFeedback(user);
			return true;
		}
	},
	filters: {
        truncate(number){
            return Number((number*100).toFixed(0)) + ' %';
        },
	},
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
p.feedback, p.give-feedback {
	float: right;
    margin-bottom: 0;
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
</style>
