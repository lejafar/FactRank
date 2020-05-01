### Wat is FactRank?

FactRank is een gratis tool die uit verslagen van parlementaire debatten en uit andere 
Nederlandstalige teksten automatisch beweringen filtert die een factcheck waard zijn. Op dit moment zoekt FactRank in de verslagen van het Vlaamse, Belgische en Nederlandse parlement, in de tweets van Vlaamse en Nederlandse parlementsleden, en in de ondertitels van de VRT-duidingsprogramma’s Terzake en De Afspraak.

FactRank rangschikt beweringen op volgorde van ‘checkwaardigheid’: bovenaan staan beweringen die zowel feitelijk zijn als maatschappelijk relevant. 

FactRank laat ook toe om [eigen tekst](/tool) in te voeren en te laten doorzoeken op checkwaardige beweringen. De tekst wordt opgesplitst in individuele beweringen waarvan de checkwaardigheid wordt beoordeeld. Ook kijkt FactRank of het een bewering kan matchen aan een reeds gepubliceerde factchecks in [Knack](https://www.knack.be/nieuws/factchecker/), [Factcheck Vlaanderen](https://factcheck.vlaanderen/) en [Nieuwscheckers](https://nieuwscheckers.nl/).

Tools als FactRank bestonden al voor Engelste teksten (bijvoorbeeld [Claimbuster](https://idir.uta.edu/claimbuster/)). Hier is hij nu ook voor het Nederlandse taalgebied.

### Wat is FactRank niet?

FactRank is geen automatische factchecker: de tool rangschikt uitspraken op volgorde van checkwaardigheid, niet van betrouwbaarheid of juistheid. 

Ook is FactRank niet perfect: het systeem leert voortdurend bij - en u kunt het helpen. Indien u beweringen ziet die volgens u een hogere of lagere plaats verdienen dan de tool eraan heeft toegekend, kunt u klikken op het <icon class="feedback" name="search" scale="1" /> icoontje indien u vindt dat de uitspraak een factcheck waard is, of op het <icon class="feedback" name="trash" scale="1" /> icoontje indien u vindt dat de uitspraak geen factcheck waard is.

### Hoe kan ik FactRank gebruiken?

Factcheckers, journalisten, onderzoekers en anderen – u, kortom, kunt FactRank op verschillende manieren gebruiken:
- als tool om efficiënt grote aantallen beweringen te [doorzoeken](/rank) op bruikbaarheid voor een factcheck. Vul een zoekterm in, selecteer een land (🇧🇪/🇳🇱), een periode, etc.
- als database van beweringen die zijn gecheckt door [Knack](https://www.knack.be/nieuws/factchecker/), [Factcheck Vlaanderen](https://factcheck.vlaanderen/) en [Nieuwscheckers](https://nieuwscheckers.nl/).
- als tool om Nederlandstalige teksten (bijvoorbeeld interviews of speeches) die u [zelf invoert](/tool) te doorzoeken op beweringen die het checken waard zijn. 
- ten slotte biedt FactRank de unieke mogelijkheid om [op trefwoord te zoeken](/rank?type=VRT_TERZAKE,VRT_DE_AFSPRAAK) in bijvoorbeeld de ondertitels van de VRT-actualiteitsprogramma’s Terzake en De Afspraak of in tweets van alle Nederlandse en Vlaamse parlementsleden.

Hiermee zijn de mogelijke toepassingen van FactRank niet uitgeput: als u de tool op een andere manier benut, [horen we het graag](/contact).

### Hoe werkt FactRank?

FactRank gebruikt een deep-learning model getraind op duizenden uitspraken, die handmatig gelabeld zijn door studenten van de Universiteit Leiden, die op hun beurt werden opgeleid door experten op het gebied van journalistiek en factchecken.

We hebben ervoor gezorgd dat FactRank zichzelf kan blijven verbeteren door feedback van gebruikers te verzamelen. Die zorgt in combinatie met periodieke hertraining van het deep-learning model, voor een continue verbetering. Een uitgebreidere verantwoording vindt u in ons artikel [FactRank: Developing Automated Claim Detection for Dutch-Language Fact-Checkers](https://people.cs.kuleuven.be/~bettina.berendt/FactRank/).

### Wie heeft FactRank gemaakt?

FactRank begon als project van Brecht Laperre, Ivo Merchiers en [Rafael Hautekiet](https://github.com/lejafar), die als studenten Computerwetenschappen aan de KU Leuven deelnamen aan de cursus Knowledge and the Web van prof. dr. Bettina Berendt. Hun doel was een tool te ontwikkelen tegen nepnieuws en misinformatie. 

Als eerste stap ontwikkelden ze een algoritme dat automatisch feitelijke beweringen kon identificeren die een factcheck waard waren. Als zulke beweringen betrouwbaar kunnen worden geïdentificeerd, kunnen ze worden doorgestuurd naar het volgende stadium van het factcheckproces, waarin ze worden geverifieerd. 

Voor de detectie van ‘checkwaardige’ claims werd een machine learning systeem op basis van [1800 met de hand geclassificeerde beweringen](https://github.com/factrank/FactRank/blob/master/data/sentences_dump_28.12.csv) getraind om van beweringen te voorspellen hoe waarschijnlijk het was dat ze checkwaardig zijn. 

Dit leverde een werkend prototype op dat gedurende 2019 werd verbeterd: de tool is nauwkeuriger en put uit een grotere dataset gelabelde beweringen. Dit is mogelijk gemaakt door een [subsidie](https://www.vlaamsjournalistiekfonds.be/500000-euro-subsidie-voor-innoverende-journalistiek) van € 39.869 die FactRank in december 2018 ontving van het Vlaams Journalistiek Fonds. 

Deze nieuwe fase van het project, die in maart 2020 werd afgesloten, is het resultaat van Vlaams-Nederlands teamwork. Onder leiding van freelancejournalist dr. Jan Jagers (factchecker van [Knack Magazine](https://www.knack.be) en [docent journalistiek](https://www.vub.ac.be/people/jan-jagers) aan de Vrije Universiteit Brussel) werkten mee: [dr. Peter Burger](https://www.universiteitleiden.nl/en/staffmembers/peter-burger#tab-1) en [dr. Alexander Pleijter](https://www.universiteitleiden.nl/medewerkers/alexander-pleijter#tab-1) (Nieuwscheckers.nl, Universiteit Leiden), [prof. dr. Peter Van Aelst](https://www.uantwerpen.be/nl/personeel/peter-vanaelst/) (Universiteit Antwerpen), [prof. dr. Bettina Berendt](https://people.cs.kuleuven.be/~bettina.berendt/) (KU Leuven en TU Berlijn) en machine learning engineer [Rafael Hautekiet](https://github.com/lejafar).

![logo_vjf](/assets/logo_VJF.jpg)
