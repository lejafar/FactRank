<template>
  <div>
    <b-container>
      <api />
    </b-container>
  </div>
</template>

<script>
import Api from "@/components/Api";

export default {
  name: "Tool",
  components: {
    api: Api,
  },
};
</script>
