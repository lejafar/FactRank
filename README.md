# FactRank

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
