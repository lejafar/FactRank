<template>
    <main>
      <vue-markdown>
**FactRank** is an online and free-to-use software tool that aims to **automatically distill checkworthy statements** from full-text transcripts **in Dutch**. The current version `{{$api_version}}` - [the demo](#demo) - already does this, and as our tests on Flemish parliament debates show, with good-quality results. But the tool needs to get better and more comprehensive, in order to be of day-to-day use for the public and fact-checkers in professional journalism.

## The road to Factrank 1.0

Factrank needs to get better and more comprehensive, in order to be of day-to-day use for the public and fact-checkers in professional journalism. This is exactly what we are working on at the moment. In December 2018, FactRank was awarded a [grant](https://www.vlaamsjournalistiekfonds.be/500000-euro-subsidie-voor-innoverende-journalistiek) of € 39.869 by the Vlaams Journalistiek Fonds to fullfill that task by March 2020. The project is teamwork. Led by freelance journalist Jan Jagers ([fact-checker](https://www.knack.be/nieuws/factchecker/) Knack Magazine / [Free University of Brussels](https://www.vub.ac.be/people/jan-jagers)). A full collaboration with [Peter Burger](https://www.universiteitleiden.nl/en/staffmembers/peter-burger#tab-1) and [Alexander Pleijter](https://www.universiteitleiden.nl/medewerkers/alexander-pleijter#tab-1) ([Nieuwscheckers.nl](https://nieuwscheckers.nl/), Leiden University, [Peter Van Aelst](https://www.uantwerpen.be/nl/personeel/peter-vanaelst/) (University of Antwerp), [Bettina Berendt](https://people.cs.kuleuven.be/~bettina.berendt/) (Leuven University) and machine learning engineer [Rafael Hautekiet](https://github.com/lejafar).

![logo_vjf](/assets/logo_VJF.jpg)

## Earlier work

The project was originally created during the course Knowledge and the Web by prof. Bettina Berendt at KU Leuven where our[^1] goal was to come up with a method to help clamping down on **Fake news and the spread of misinformation**. As a starting point, we set out to develop an algorithm that would automatically **identify** interesting claims that are worth checking i.e. **Check-worthy Factual Statements**[^2]. Only when such statements can be reliably identified, can they be sent to the next step in the pipeline that actually tries to falsify the interesting claims.


[^1]: Back then, it was developped by Brecht Laperre, Ivo merchiers and [Rafael Hautekiet](https://github.com/lejafar)
[^2]: This terminology is also used by [the Claimbuster-project](http://idir-server2.uta.edu/claimbuster/), a big source of inspiration during the project.

A classifier was trained using on **1800** hand-classified **statements** in order to predict the probability of check-worthiness when provided with a statement. A demonstration of its current ability can be found on the [front page](/#/) in the from of a rank of Dutch statements made during the last Plenary Meeting of the Belgian Federal parliament based on their check-worthiness. To provide you with the ability to play around with input of your own and see how this is interpreted by FactRank, we made a little [demo](/#/demo).

</vue-markdown>

    </main>
</template>

<script>
export default {
  name: 'About',
  data () {
    return {
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
section.footnotes{
    font-size: .9rem;
}
section.footnotes p {
    margin-bottom: .5rem;
}
.footnote-backref{
    display:none;
}
img {
    max-width: 60%;
}
</style>
