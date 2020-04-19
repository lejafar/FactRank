### FactRank API

We have an open API with a rate limit of 200 requests a day and 50 requests per hour.

#### `/` endpoint

This endpoint allows one to send a text, which is split into statements and ranked according to their check-worthiness <kbd>score</kbd>. 

When a statement can be matched to an existing fact-check it will also be returned.

<div v-highlight >
<pre class="language-bash"><code>curl -X POST https://api-v2.factrank.org/ \
	 -H "Content-Type: application/json" \
	 -d '{"text": "Een Arm kind heeft meer kans op een C-attest. \
                   Maar daar geloof ik persoonlijk niet veel van."}'
</code></pre>
<pre class="language-javascript"><code>[
  {
    "content": "Een Arm kind heeft meer kans op een C-attest.",
    "context": {},
    "match": {
      "conclusion": "GROTENDEELS_WAAR",
      "confidence": 0.9105110168457031,
      "matched": true,
      "statement": "Een kind uit een arm gezin heeft zeven keer meer kans op een C-attest.",
      "url": "https://www.knack.be/nieuws/factchecker/factcheck-een-kind-uit-een-arm-gezin-heeft-zeven-keer-meer-kans-op-een-c-attest/article-longread-1580425.html"
    },
    "score": 0.9745201468467712
  },
  {
    "content": "Maar daar geloof ik persoonlijk niet veel van.",
    "context": {},
    "match": {
      "matched": false
    },
    "score": 0.00037305636215023696
  }
]</code></pre>
</div>
