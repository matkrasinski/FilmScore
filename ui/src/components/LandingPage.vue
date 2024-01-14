<template>
  <div id="team" class="bg-slate-50 w-full shadow-md">
    <div class="container py-32">
      <div class="grid place-items-center w-full grid-cols-1 gap-32 md:grid-cols-2 lg:grid-cols-4 my-32 text-center">
        <movie-tile v-for="movie in this.movies.slice(0, 20)" :key="movie" :movie="movie"/>
      </div>       
    </div>
  </div>
</template>

<script>
import MovieTile from './MovieTile.vue'
import axios from 'axios'

export default {
  name: "LandingPage",
  components: {
    MovieTile
  },
  data() {
    return {
      movies: []
    }
  }, 
  mounted() {
    this.loadMovies()
  },
  methods: { 
    async loadMovies() {
      axios.get("http://localhost:5000/data/movies")
      .then(response => {
        this.movies = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    }
  }
}
</script>