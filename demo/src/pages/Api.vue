<template>
  <b-container>
    <main>
      <api-nl v-if="this.$i18n.locale.includes('nl')" />
      <api-en v-else />
    </main>
  </b-container>
</template>

<script>
import ApiEN from "@/content/en/api.md";
import ApiNL from "@/content/nl/api.md";

export default {
  name: "Api",
  components: {
    "api-en": ApiEN,
    "api-nl": ApiNL,
  },
};
</script>
