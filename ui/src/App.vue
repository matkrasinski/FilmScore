<template>
  <div>
    <default-navbar/>
    <router-view/>
  </div>
</template>

<script>
import DefaultNavbar from './layout/DefaultNavbar.vue'

export default {
  name: 'App',
  components: { DefaultNavbar }, 
}
</script>

<style>
/* #app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
} */
</style>
