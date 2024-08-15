<template>
  <div id="app">
    <div class="header">
      <HomeHeader ref="homeheader"></HomeHeader>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
import HomeHeader from './components/HomeHeader.vue';
export default {
  components: {
    HomeHeader
  },
  mounted() {
    this.$router.push({
      path: '/'
    })
  }
}

</script>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  width: 100%;
  height: 100vh;

  .header {
    width: 100%;
    height: 60px;
  }
}
</style>
