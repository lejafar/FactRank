<template>
  <div class="hello">
    <vue-markdown>

    FactRank was created as a project for the course *Knowledge and the Web* by prof. Bettina Berendt at KU Leuven and is written and maintained by:

    - Brecht Laperre (brecht.laperre@student.kuleuven.be)
    - Ivo merchiers (ivo.merchiers@student.kuleuven.be)
    - Rafael Hautekiet (rafaelhautekiet@student.kuleuven.be)

    You can always contact us for questions or suggestions.
    If you find any bugs, please file a bug report on [github](https://github.com/lejafar/KaW-project/issues).

    Our API is openly available on https://api.factrank.org/, a minimal example:

    ```javascript
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
    ```
  </vue-markdown>
  </div>
</template>

<script>
export default {
  name: 'Contact',
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
<style>
pre{
  background-color: #f6f8fa;
  padding: 20px;
  border-radius: 5px;
}
</style>
