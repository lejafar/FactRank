<template>
  <span>
    <span v-if="speaker" class="speaker">
      {{ speaker.country | flag(source.name) }}
      {{ speaker.name | cleanName }}
      <cite v-if="speaker && speaker.association" title="Speaker">
        ({{ speaker.association.name }})
      </cite>
    </span>
    <span v-else-if="source.is_factcheck == 1" class="speaker factchecked">
      <a class="source_type text-secondary" :href="source.url" target="_blank">
        <b-badge pill variant="primary">
          <icon class="search" name="search" scale="1" />
          FactCheck Available
          <icon name="link" class="link" size="xs" />
        </b-badge>
      </a>
    </span>
    <span v-else class="speaker">
      <b>{{ source.name.split("2")[0] }}</b>
      {{ formatDate(source.published_at, true) }}
    </span>
  </span>
</template>

<script>
import utilMixin from "@/mixins/utilMixin";

export default {
  name: "SpeakerInfo",
  props: ["speaker", "source"],
  mixins: [utilMixin],
  filters: {
    cleanName(name) {
      return name
        .replace("De heer", "")
        .replace("Mevrouw", "")
        .replace("Minister", "");
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
.badge-primary {
  background-color: #1976d2;
}
</style>
