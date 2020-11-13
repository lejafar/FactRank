### What is FactRank?

FactRank is a free tool that automatically identifies factual claims that are worthy of a fact-check. Currently, FactRank searches these claims in transcripts of the Flemish, Belgian and Dutch parliaments, in tweets of Flemish and Dutch politicians, and in subtitles of the Flemish public television broadcaster VRT’s news-analysis programmes Terzake and De Afspraak.

FactRank sorts claims by their "check-worthiness". Thus, at the top you'll find claims that are factual as well as they hold social relevance.

FactRank also allows you to scan [your own text sources](/tool) for check-worthy factual statements. It will split the text in individual statements and try to match each statement to pre-existing fact-check using our database of fact-checks collected from [Knack](https://www.knack.be/nieuws/factchecker/), [Factcheck Vlaanderen](https://factcheck.vlaanderen/) and [Nieuwscheckers](https://nieuwscheckers.nl/).

Tools like FactRank already exist for other languages, one example is [Claimbuster](https://idir.uta.edu/claimbuster/).

### What is FactRank not?

FactRank is not an automated fact-checker. The tool ranks statements only by their check-worthiness, not by their reliability or correctness.

FactRank is also not perfect. The system keeps on learning – and you can help. If you see a claim that you think deserves a higher or lower position in the ranking than the one given by the tool, you can click            <icon class="feedback" name="search" scale="1" /> icon if you think it is worth a fact-check of the <icon class="feedback" name="trash" scale="1" /> icon if you think it is not worth a fact-check.

### How can I use FactRank?

Fact-checkers, journalists, researchers, and others – whoever feels like it – can use FactRank in several ways:
- As a tool to [search](/rank) a large number of sources for useful claims to fact-check. Enter a search term, select the country (🇧🇪/🇳🇱), time period, etc.
- As a database of claims that have already been fact-checked by [Knack](https://www.knack.be/nieuws/factchecker/), [Factcheck Vlaanderen](https://factcheck.vlaanderen/) and [Nieuwscheckers](https://nieuwscheckers.nl/).
- As a tool to search for check-worthy claims in Dutch-language texts that [you enter yourself](/tool) (for example interviews or speeches).
- Last but not least, FactRank also offers the unique possibility to [do keyword searches](/rank?type=VRT_TERZAKE,VRT_DE_AFSPRAAK) in the subtitles of the Flemish public television broadcaster VRT’s news-analysis programmes Terzake and De Afspraak and in the tweets of all Dutch and Flemish members of parliament.

This is not an exhaustive list of all possible applications of FactRank. If you use the tool in a different way, we’d love to hear from you. Please [contact](/contact) us.

### How does FactRank work?

FactRank uses a deep-learning model that has been trained on thousands of statements, manually labeled by students of the University of Leiden in turn trained by experts in the field of fact-checking.

We've also made sure to "close the loop" in that we collect user feedback which - using periodic retraining of the deep-learning model - results in continuous self-improvement. You can find a more in-depth description in our article [FactRank: Developing Automated Claim Detection for Dutch-Language Fact-Checkers](https://people.cs.kuleuven.be/~bettina.berendt/FactRank/).

### Who created FactRank?

FactRank began as a term project of Brecht Laperre, Ivo Merchiers and [Rafael Hautekiet](https://github.com/lejafar), in the course Knowledge and the Web offered by Prof. Dr. Bettina Berendt at the Department of Computer Science at the University of Leuven. Their goal was to develop a tool that would help the fight against fake news and the spread of misinformation.

As a first step, they developed a machine learning model that was able to automatically detect check-worthy factual statements. If such claims can be reliably identified, they can be forwarded to a fact-checking process for verification. The model was trained on 1800 [manually classified statements](https://github.com/factrank/FactRank/blob/master/data/sentences_dump_28.12.csv).

This yielded a working prototype, which was improved during the course of 2019. The tool is now more accurate and draws on a larger dataset of ~7000 labeled statements. This was made possible by a [grant](https://www.vlaamsjournalistiekfonds.be/500000-euro-subsidie-voor-innoverende-journalistiek) of € 39.869 that was awarded to FactRank by the Vlaams Journalistiek Fonds in December 2018.

This new phase of the project, which was finalised in March 2020, is the result of Flemish-Dutch teamwork. Led by freelance journalist Dr. Jan Jagers (fact-checker of [Knack Magazine](https://www.knack.be) and [lecturer in journalism](https://www.vub.ac.be/people/jan-jagers) at Vrije Universiteit Brussel) the team also comprised [Dr. Peter Burger](https://www.universiteitleiden.nl/en/staffmembers/peter-burger#tab-1) and [Dr. Alexander Pleijter](https://www.universiteitleiden.nl/medewerkers/alexander-pleijter#tab-1) (Nieuwscheckers.nl, University of Leiden), [Prof. Dr. Peter Van Aelst](https://www.uantwerpen.be/nl/personeel/peter-vanaelst/) (University of Antwerp), [Prof. Dr. Bettina Berendt](https://people.cs.kuleuven.be/~bettina.berendt/) (KU Leuven and TU Berlin, Germany), and machine learning engineer [Rafael Hautekiet](https://github.com/lejafar).

![logo_vjf](/assets/logo_VJF.jpg)
