### FactRank API

Wij bieden een open API aan met een limiet van 200 aanvragen per dag.

#### `/` endpoint

Dit endpoint laat toe om text te versturen, die vervolgens wordt opgesplits in individuele beweringen en gesorteerd volgens checkwaardigheids <kbd>score</kbd>. 

Wanneer een bewering kan gematched worden aan een reeds gepubliceerde fact-check uit onze database wordt deze ook teruggegeven.

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


