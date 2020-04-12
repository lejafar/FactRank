### What is FactRank?

FactRank is a free tool that automatically identifies factual claims that are worthy of a fact-check, in transcripts of parliamentary debates and other Dutch-language texts. Currently, FactRank searches through the transcripts from the Flemish, Belgian and Dutch parliaments, through the tweets of Flemish and Dutch members of parliament, and through the subtitles of the Flemish public television broadcaster VRT’s news-analysis programmes Terzake and De Afspraak.

FactRank orders claims by ‘check-worthiness’. Thus, at the top of the results list you will find claims that are factual as well as societally relevant.

You can also use the tool to search the reports of the Flemish fact-checking organisation [Factcheck Vlaanderen](https://factcheck.vlaanderen/). These reports contain claims that have already been assessed for veracity by (human) fact-checkers.

Tools like FactRank already exist, especially for English-language texts (one example is [Claimbuster](https://idir.uta.edu/claimbuster/)). Now there is also one for the Dutch language. 

### What is FactRank not?

FactRank is not a fact-checker. The tool ranks statements only by their check-worthiness, not by their reliability or correctness.

FactRank is not perfect. The system keeps on learning – and you can help. If you see a claim that you think deserves a higher or lower position in the ranking than the one given by the tool, you can ‘upvote’ or ‘downvote’ it (“I think this statement is check-worthy / NOT check-worthy’’).

### How can I use FactRank? 

Fact-checkers, journalists, researchers, and others – whoever feels like it – can use FactRank in several ways:  
- As a tool to filter large numbers of claims for their usefulness for a fact-check. Enter one or more search terms and select the country (the Netherlands or Flanders/Belgium) as well as the time period you are interested in. 
- As a database of claims that have already been fact-checked by [Factcheck Vlaanderen](https://factcheck.vlaanderen/), a collaboration of Flemish universities, companies and media.
- As a tool to filter out check-worthy claims from Dutch-language texts that you enter yourself (for example interviews or speeches). Please note that the tool has been trained on texts of parliamentary debates and will therefore perform best on such materials.
- Last but not least, FactRank also offers the unique possibility to do keyword searches in the subtitles of the Flemish public television broadcaster VRT’s news-analysis programmes Terzake and De Afspraak and in the tweets of all Dutch and Flemish members of parliament.

This is not an exhaustive list of all possible applications of FactRank. If you use the tool in a different way, we’d love to hear from you. Please <a href="mailto:jan.jagers@gmail.com" target="_top">e-mail</a> Jan Jagers, the project leader

### How does FactRank work?

FactRank is based on a combination of thousands of manually classified statements, taken from parliamentary debates and journalistic interviews with politicians, and a machine learning algorithm. Thus, the system leverages the judgements of experts in journalism and fact-checking, it learns from them, and it applies what it learned to new statements.

Both components remain active: FactRank is continuously being fed new material, and users can improve the system by correcting the classification of individual claims. You can find a more in-depth description in our article FactRank: [Developing Automated Claim Detection for Dutch-Language Fact-Checkers](https://people.cs.kuleuven.be/~bettina.berendt/FactRank/).

### Who created FactRank?

FactRank began as a term project of computer science students Brecht Laperre, Ivo Merchiers and Rafael Hautekiet, in the course Knowledge and the Web offered by Prof. Dr. Bettina Berendt at the Department of Computer Science at the University of Leuven. Their goal was to develop a tool against fake news and misinformation.

As a first step, they developed an algorithm that was able to automatically detect check-worthy factual statements. If such claims can be reliably identified, they can be forwarded to a fact-checking process for verification.

For the detection of check-worthy claims, a machine learning system was trained on 1800 [manually classified statements](https://github.com/factrank/FactRank/blob/master/data/sentences_dump_28.12.csv), in order to predict their likelihood of being checkworthy. 

This yielded a working prototype, which was improved in 2019/20. The tool is now more accurate and draws on a larger number of sources. This was made possible by a [grant](https://www.vlaamsjournalistiekfonds.be/500000-euro-subsidie-voor-innoverende-journalistiek) of € 39.869 that FactRank was awarded by the Vlaams Journalistiek Fonds in December 2018.

This new phase of the project, which was finalised in March 2020, is the result of Flemish-Dutch teamwork. Led by freelance journalist Dr. Jan Jagers (fact-checker of Knack Magazine and lecturer in journalism at Vrije Universiteit Brussel) the team also comprised Dr. Peter Burger and Dr. Alexander Pleijter (Nieuwscheckers.nl, University of Leiden), Prof. Dr. Peter Van Aelst (University of Antwerp), Prof. Dr. Bettina Berendt (KU Leuven and TU Berlin, Germany), and  machine learning engineer Rafael Hautekiet.

![logo_vjf](/assets/logo_VJF.jpg)
