<template>
  <div id="app">
    <menubar/>
    <b-container>
      <router-view></router-view>
    </b-container>
  </div>
</template>

<script>
import MenuBar from './components/MenuBar'

export default {
  name: 'app',
  components: {
    'menubar': MenuBar
  }
}
</script>

<style>

</style>
