# FactRank

**Fake news and the spread of misinformation** is nothing new. But, due to recent events, both Google and Facebook are trying to clamp down on the problem. Automated end-to-end fact-checking can play a crucial role in this fight and [the Claimbuster-project](http://idir-server2.uta.edu/claimbuster/) has paved the way for developing this system for the English language.

The starting point for any fact-checking process is the **identification of** interesting claims or statements that present facts. These kinds of sentences are defined as **Check-worthy Factual Statement**. Only when such sentences can be reliably identified, can they be sent to the next step in the pipeline that actually tries to falsify the interesting claims.

The goal of this project to take the first step towards developing such a fact-checking system for the Dutch language, with a focus on identifying Check-worthy Factual Statements.  A classifier was trained using a linear classifier on **800 hand-classified statements** and later calibrated in order to predict the probability of check-worthiness when provided with a statement. A demonstration of its current ability can be found on http://factrank.org/ in the form of a automated ranking of Dutch statements made during the last Plenary Meeting of the Belgian parliament based on their check-worthiness.

## Classifier

![confusion matrix](cnf_matrix.svg)

## Project Structure

```
├── demo
|     └─ Vue.js front-end to provide insight in prediction process
|
├── helper.py
|     └─ Custom feature transformer classes allowing for easy predictions
├── extractor.py
|     └─ Exctractor class enables retrieving all nlp features from `sentence`
|
├── learner.py
|     └─ Preprocess data, construct pipeline, train SVM and export model.
└── parser.py
|     └─ Parse latest transcript of plenary meeting, detect Check-Worthy statements
|        and save predictions together with feedback to be served on demo page.
|
└── endpoint.py
      └─ Load pre-trained model and provide endpoint for predictions.
```
