<template>
  <div class="hello">
    <vue-markdown>

    FactRank is written and maintained by:

    - Brecht Laperre (brecht.laperre@student.kuleuven.be)
    - Ivo merchiers (ivo.merchiers@student.kuleuven.be)
    - Rafael Hautekiet (rafaelhautekiet@student.kuleuven.be)

    You can always contact us for questions or suggestions.
    If you find any bugs, please file a bug report on [github](https://github.com/lejafar/KaW-project/issues).

    We have an open api at https://api.factrank.org/sentence
  </vue-markdown>
  <pre>

    makePrediction (input) {
      fetch("https://api.factrank.org/sentence", {
        body: JSON.stringify(input),
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      }).then(response => response.json())
        .then((data) => {
          // returns list of predictions
          console.log(data.predictions);
        })
    }

    </pre>
  </div>
</template>

<script>
import VueMarkdown from 'vue-markdown'

export default {
  name: 'Contact',
  components: {
    'vue-markdown': VueMarkdown
  },
  props: [
    'name'
  ],
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
pre{
  background-color: #f6f8fa;
}
</style>
