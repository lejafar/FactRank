<template>
  <b-container>
    <main>
      <about-nl v-if="this.$i18n.locale.includes('nl')" />
      <about-en v-else />
    </main>
  </b-container>
</template>

<script>
import AboutEN from "@/content/en/about.md";
import AboutNL from "@/content/nl/about.md";

export default {
  name: "About",
  components: {
    "about-en": AboutEN,
    "about-nl": AboutNL,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
section.footnotes {
  font-size: 0.9rem;
}

section.footnotes p {
  margin-bottom: 0.5rem;
}

.footnote-backref {
  display: none;
}

img {
  max-width: 60%;
}
</style>
