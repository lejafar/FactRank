<template>
  <footer class="footer">
    <b-container>
      <p><span v-html="$t('footer.made.rafael')"/>, <span v-html="$t('footer.made.comissioned')"/></p>
      <p v-html="$t('footer.feedback')"></p>
    </b-container>
  </footer>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
  color: #b4bbc1;
}
.footer {
  padding-top: 2.5rem;
  padding-bottom: 2rem;
  background-color: #f5f5f5;
}
</style>
<style>
footer a {
  color: #1976d2 !important;
  text-decoration: underline;
}
</style>
