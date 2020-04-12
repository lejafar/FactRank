<template>
    <b-container>
		<p>Made with ❤️ in Borgerhout by Rafael Hautekiet, comissioned by Feitsj VZW</p>
        <vue-markdown>{{ $t('footer.feedback') }}</vue-markdown>
    </b-container>
</template>

<script>
export default {
  name: "Footer",
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.container {
	margin-top: 2rem;
	margin-bottom: 2rem;
	color: #b4bbc1;
}
</style>
<style>
.container > div > p > a {
  color: #1976d2 !important;
  text-decoration: underline;
}
</style>
