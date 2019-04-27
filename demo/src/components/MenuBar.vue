<template>
  <b-navbar toggleable="md" type="light" variant="light">
    <b-container>
    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <b-navbar-brand href="#">FactRank</b-navbar-brand><b-badge pill variant="warning">{{$api_version}}</b-badge>
    <b-collapse is-nav id="nav_collapse">

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">

        <b-navbar-nav>
          <b-nav-item to="/" exact>Rank</b-nav-item>
          <b-nav-item to="/about">About</b-nav-item>
          <b-nav-item to="/press">Press</b-nav-item>
          <b-nav-item href="https://github.com/lejafar/factrank"><icon name="brands/github" /></b-nav-item>
        </b-navbar-nav>
        <b-button variant="outline-primary" to="/demo" id="try_it">Try it!</b-button>

      </b-navbar-nav>
    </b-collapse>
  </b-container>
  </b-navbar>
</template>

<script>
export default {
  name: 'MenuBar',
  data () {
    return {
      msg: 'About us ...'
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar-brand{
  font-size: 25px;
  font-weight: 700;
  font-style: italic;
}
.navbar{
  margin-bottom: 2rem;
}
#try_it{
  margin-left: 1rem;
}
</style>
