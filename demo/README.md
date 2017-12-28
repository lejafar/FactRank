# factrank

> Dutch Check-Worthy Detection

We attempt to classify Dutch tweets from Belgian politicians based on their check-worthyness. For this we follow the general approach taken by Claimbuster.
The data will be gathered using the twitter API. The gathered data set will be manually classified in three categories:

- Non-factual Sentence **(NFS)**,
- Unimportant Factual Sentence **(UFS)**,
- Check-worthy Factual Sentence **(CFS)**, whilst irrelevant tweets (emoticons, too short, not containing coherent sentences...) will be discarded.

For the manual classification we will use a set of general guidelines. To verify that our judgement is similar, we will individually analyse the same, small dataset, allowing us to check our Inter-rater agreement (and change our guidelines if necessary).
From the tweets we will extract a range of features, inspired by the Claimbuster feature importance. Example features are:

- Sentiment (eg. using https://www.clips.uantwerpen.be/pages/sentiment-analysis-for-dutch)
- Sentence length
- Parts of Speech (eg. https://languagemachines.github.io/frog/)

These features will then be inserted in a learning algorithm. We will certainly use SVM, as this was the most successful for Claimbuster, but other learning algorithms could also be considered. Especially an algorithm that gives interpretable results would be very interesting.
