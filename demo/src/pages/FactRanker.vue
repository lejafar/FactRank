<template>
  <div>
    <b-container>
      <ranker />
    </b-container>
  </div>
</template>

<script>
import Ranker from "@/components/Ranker";

export default {
  name: "FactRanker",
  components: {
    ranker: Ranker
  },
};
</script>

