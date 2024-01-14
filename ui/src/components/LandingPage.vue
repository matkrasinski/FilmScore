<template>
  <div id="team" class="bg-gray-50 w-full shadow-md">
      <div class="container py-32">
          <div class="grid place-items-center w-full grid-cols-1 gap-64 md:grid-cols-2 lg:grid-cols-4 my-32 text-center">
              <movie-tile v-for="movie in this.movies.slice(0, 10)" :key="movie" :movie="movie">
                <a> {{ movie.original_title }} </a>
              </movie-tile>
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
      data: [1,2,3,4,5,66,7,134,123,1],
      movies: []
    }
  }, 
  mounted() {
    this.loadMovies()
    console.log(this.movies)
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
    MovieTile