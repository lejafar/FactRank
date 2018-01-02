<template>
  <blockquote class="blockquote">
    <footer v-if="sentence.speaker" class="blockquote-footer">{{sentence.speaker}}
      <cite title="Speaker">({{sentence.party}})</cite>
    </footer>
    <p class="mb-0">
      <template v-for="(word, index) in sentence.feedback.words" >
        <span :id="'id'+sentence.sentence_id+'key'+word+index" :class="getClass(sentence.feedback.inline, index)">{{word}}</span>
        <span :class="innerClass(sentence.feedback.inline, index)" v-if="hasInnerClass(sentence.feedback.inline, index)">&nbsp;</span>
        <span v-else-if="nextPunct(sentence.feedback.words, index)"></span>
        <span v-else>&nbsp;</span>
        <b-tooltip v-if="getInfo(sentence.feedback.inline,sentence.feedback.legend, index).length" :target="'id'+sentence.sentence_id+'key'+word+index">
          {{ getInfo(sentence.feedback.inline,sentence.feedback.legend, index) }}
        </b-tooltip>
      </template>
    </p>
  </blockquote>
</template>

<script>
export default {
  name: 'SentenceExtended',
  props: ['sentence'],
  data () {
    return {
    }
  },
  methods: {
    getClass(inline, i){
      var fb_class = ''
      if (inline.word_combo[i]){
        fb_class += "word_combo "
      }else if (inline.word[i]){
        fb_class += "word "
      }
      if (inline.lempos_combo[i]){
        fb_class += "lempos_combo "
      }else if (inline.lempos[i]){
        fb_class += "lempos "
      }
      if (inline.pos_combo[i]){
        fb_class += "pos_combo "
      }else if (inline.pos[i]){
        fb_class += "pos "
      }
      return fb_class
    },
    getInfo(inline,legend, i){
      var fb = []
      if (inline.word_combo[i]){
        fb.push("combination of characteristic words")
      }else if (inline.word[i]){
        fb.push("a characteristic word")
      }
      if (inline.lempos_combo[i]){
        fb.push("combination of characteristic lemma's with specific Part-Of-Speech tags")
      } else if (inline.lempos[i]){
        fb.push("a characteristic lemma with specific Part-Of-Speech tag ("+legend.lempos_legend[i]+")")
      }
      if (inline.pos_combo[i]){
        fb.push("combination of characteristic consecutive Part-Of-Speech tags")
      } else if (inline.pos[i]){
        fb.push("a characteristic Part-Of-Speech tag ("+legend.pos_legend[i]+")")
      }

      var info = ""
      for (var i=0; i<fb.length; i++) {
        info += fb[i]
        if(i+1 == fb.length-1) info += ", and "
        else if(i+1 < fb.length-1) info += ", "
      }
      // Capitalize first letter
      info = info.charAt(0).toUpperCase() + info.slice(1);
      return info
    },
    nextPunct(words, i){
      return i + 1 < words.length && (words[i+1] == ',' || words[i+1] == '.')
    },
    innerClass(inline, i){
      var inner_fb_class = ''
      if (i + 1 < inline.word_combo.length && inline.word_combo[i]) {
        inner_fb_class += inline.word_combo[i + 1] ? "word_combo " : ""
      }
      if (i + 1 < inline.lempos_combo.length && inline.lempos_combo[i]) {
        inner_fb_class += inline.lempos_combo[i + 1] ? "lempos_combo " : ""
      }
      if (i + 1 < inline.pos_combo.length && inline.pos_combo[i]) {
        inner_fb_class += inline.pos_combo[i + 1] ? "pos_combo " : ""
      }
      return inner_fb_class
    },
    hasInnerClass(inline, i){
      return this.innerClass(inline, i) != ""
    }
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

.word_combo, .word{
  font-weight: bold;
}
.lempos_combo, .lempos{
  background-color: #ffc107;
}
.pos_combo, .pos{
  font-style: italic;
}
.pos_combo{
  /* border-bottom: solid 1.5px #CFD8DC;
  padding-bottom: .07rem; */
 text-decoration: underline;
}

span{
  font-size: 1rem;
}
p.mb-0{
  font-size: 0rem;
}
</style>
