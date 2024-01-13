<template>
  <div class="container">
    <table class="table table-zebra table-xs" style="overflow-x: auto;">
      <thead>
        <tr>
          <th>
            <div class="flex items-center">
              Original Title 
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Minutes
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Collection
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Genre(s) 
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Production Companies
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Date
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Spoken Languages
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Status
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Keywords
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Promotion Videos
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Average Rating
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Number of Votes
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Director(s)
            </div>
          </th>
          <th>
            <div class="flex items-center">
              Actors(s)
            </div>
          </th>
        </tr>
      </thead>
      <tbody>
        
        <tr class="hover" v-for="(movie, index) in movies.slice(0, 500)" :key="index">
          <td>{{ movie.original_title }} </td>
          <td>{{ movie.runtime }}</td>
          <td>{{ movie.belongs_to_collection }}</td>
          <td>{{ movie.genres.map(String).join(", ") }}</td>
          <td>{{ movie.production_companies.map(String).join(", ") }}</td>
          <td>{{ movie.release_date }}</td>
          <td>{{ movie.spoken_languages.map(String).join(", ") }}</td>
          <td>{{ movie.status }}</td>
          <td>{{ this.shortText(movie.keywords) }}</td>
          <td>{{ this.shortText(movie.videos) }}</td>
          <td>{{ movie.averageRating }}</td>
          <td>{{ movie.numVotes }}</td>
          <td>{{ movie.directors.map(String).join(", ") }}</td>
          <td>{{ movie.actors.map(String).join(", ") }}</td>
        </tr>
      </tbody>
    </table>
  </div>

</template>

<script>
import axios from 'axios';

export default {
  name: "MoviesPanel",
  data() {
    return {
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
    },
    shortText(text) {
      return text.length > 20 ? text.slice(0, 20) + "..." : text
    }
  }
}

</script>

<style scoped>

table {
    display: block;
    overflow-x: auto;
    /* white-space: wrap; */
}
</style>
