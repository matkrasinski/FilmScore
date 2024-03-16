<template>
  <div>
    <default-navbar/>
    <Suspense>

      <template #default>
        <router-view/>
      </template>
      <template #fallback>
        ...
      </template>
    </Suspense>
    <default-footer/>
  </div>
</template>

<script>
import DefaultFooter from './layout/DefaultFooter.vue'
import DefaultNavbar from './layout/DefaultNavbar.vue'

export default {
  name: 'App',
  components: { DefaultNavbar, DefaultFooter, }, 
}
</script>

<style scoped>
body {
  background: black;
}
</style>