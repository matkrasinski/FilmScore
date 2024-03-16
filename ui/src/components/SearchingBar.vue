<template>
  <form  @submit.prevent="handleSubmit">
    <div class="flex container">
        <div class="relative w-full">
            <input type="text" v-model="query" id="search-dropdown" class="block p-8 w-full z-0 bg-gray-50 rounded-e-lg border border-gray-300 text-3xl rounded-r-5xl rounded-l-5xl shadow-2xl" placeholder="Search for a movie">
            <button @click="console.log(this.query), $emit('search-movies', this.query)" type="button" class="absolute top-0 end-0 p-8 text-sm font-medium h-full text-white bg-emerald-500 rounded-e-lg border border-emerald-500 rounded-r-5xl shadow-2xl">
                <i class="bi bi-search text-3xl"></i>
                <span class="sr-only text-xl">Search</span>
            </button>
        </div>
    </div>
  </form>


</template>

<script>
export default {
  name: 'SearchingBar',
  data() {
    return {
      query: ""
    }
  }
}
</script>

<style scoped>
.rounded-r-5xl {
  border-top-right-radius: 3rem;
  border-bottom-right-radius: 3rem;
}

.rounded-l-5xl {
  border-top-left-radius: 3rem;
  border-bottom-left-radius: 3rem;
}

</style>