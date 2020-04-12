<template>
  <b-container>
    <main>
<vue-markdown>
- Stimuleringsfonds voor de Journalistiek (Dutch)[svdj.nl/nieuws/robot-helpt-factchecken-nieuws-doorzoeken/](https://www.svdj.nl/nieuws/robot-helpt-factchecken-nieuws-doorzoeken/)
- De Morgen 13/12/2018 (Dutch)[demorgen.be/tech-wetenschap/vlaanderen-bindt-met-technologie-de-strijd-tegen-nepnieuws](https://www.demorgen.be/tech-wetenschap/vlaanderen-bindt-met-technologie-de-strijd-tegen-nepnieuws-aan~b732defa/):
</vue-markdown>
        <pdf resize src="/assets/20181213_De-Morgen.pdf">
        <template slot="loading">
            loading ...
        </template>
        </pdf>
    </main>
  </b-container>
</template>

<script>
export default {
  name: "Press",
  data() {
    return {};
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style></style>
