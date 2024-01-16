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

<style scoped>
body {
  background: black;
}
</style>