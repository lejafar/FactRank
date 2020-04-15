<template>
  <div>
    <div
      class="spacing bg-primary-color"
      v-if="this.$route.name == 'Landing'"
    />
    <b-navbar
      toggleable="md"
      type="light"
      class="bg-primary-color secondary-color"
    >
      <b-container>
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand to="/" @click="resetQuery">
          FactRank.
        </b-navbar-brand>
        <!--<span class="subtitle"> - automatic identification of factual claims that are worthy of a fact-check -</span>-->
        <!--<b-badge v-if="$branch_version" pill variant="warning">{{$api_version}} : {{$branch_version}}</b-badge>-->
        <!--<b-badge v-else pill variant="warning">{{$api_version}}</b-badge>-->
        <b-collapse is-nav id="nav_collapse">
          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-navbar-nav>
              <b-nav-item @click="resetQuery" to="/rank" exact>Rank</b-nav-item>
              <b-nav-item to="/about">About</b-nav-item>
              <b-nav-item to="/press">Press</b-nav-item>
              <b-nav-item href="https://github.com/lejafar/factrank">
                <icon name="brands/github" />
              </b-nav-item>
            </b-navbar-nav>
            <!-- <b-button variant="outline-primary" to="/demo" id="try_it">Input text</b-button> -->
          </b-navbar-nav>
        </b-collapse>
      </b-container>
    </b-navbar>
    <div
      class="spacing bg-primary-color"
      v-if="this.$route.name == 'Landing'"
    />
  </div>
</template>

<script>
export default {
  name: "MenuBar",
  data() {
    return {
      search_query: "",
    };
  },
  methods: {
    resetQuery() {
      this.$router.push({
        query: {},
      });
      this.$router.go();
    },
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.navbar-brand {
  font-size: 40px;
  font-weight: 700;
  font-style: italic;
}

.nav-link,
.navbar-light,
.navbar-brand {
  color: #ffffff !important;
}

#try_it {
  margin-left: 1rem;
}
</style>
