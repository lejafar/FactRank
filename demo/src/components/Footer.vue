<template>
<footer class="footer">
    <b-container>
		<p>Made with ❤️ in Borgerhout by Rafael Hautekiet, comissioned by Feitsj VZW</p>
        <vue-markdown>{{ $t('footer.feedback') }}</vue-markdown>
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
.footer{
	padding-top: 2.5rem;
	padding-bottom: 2rem;
    background-color: #f5f5f5;
}
</style>
<style>
.container > div > p > a {
  color: #1976d2 !important;
  text-decoration: underline;
}
</style>
