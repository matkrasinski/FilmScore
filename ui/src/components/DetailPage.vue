<template>
<div class="bg-zinc-50 rounded-3xl items-center text-center container">
  <movie-tile
    :key="this.movie"
    :movie="this.movie"
    :margin="'280px 0% -580px 250px'"
    :circleColor="'#1f2020'"
    :scoreName="this.scoreType"
    ></movie-tile>
    <div class="my-16 ">
      
      <a :href="`https://www.imdb.com/title/${movie.imdb_id}`"
      class="mr-8 px-8 py-2 border text-5xl rounded-full font-bold bg-yellow-400 shadow-xl cursor-pointer hover:no-underline ">
        IMDb
      </a>


      <div class="mt-16">
        <label class="text-3xl mr-8">Director(s):</label>
      </div>
      <a v-for="director in movie.directors" 
      :key="director.id" 
      :href="`https://www.imdb.com/name/${director.id}`"
      class="mr-8 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl cursor-pointer hover:no-underline ">
        {{ director.name }}
      </a>

      <div class="mt-16">
        <label class="text-3xl mr-4">Actors:</label>
      </div>
      <a v-for="actor in movie.actors" 
      :key="actor.id" 
      :href="`https://www.imdb.com/name/${actor.id}`"
      class="mr-4 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl cursor-pointer hover:no-underline inline-block">
        {{ actor.name }}
      </a>

      <div class="">
        <label class="text-3xl mr-8 mt-16">Genres:</label>
      </div>
      <span v-for="genre in movie.genres" :key="genre" class="mr-8 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl">
        {{ genre }}
      </span>

      <div class="mt-16">
        <label class="text-3xl mr-4">Production companies:</label>
      </div>
      <span v-for="company in movie.production_companies" 
        :key="company.id" 
        class="mr-4 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl inline-block">
        {{ company.name }}
      </span>
      
      <div class="mt-16">
        <label class="text-3xl mr-4">Duration in minutes:</label>
        <span 
          class="mr-4 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl inline-block">
          {{ movie.runtime }}
        </span>
      </div>

      <div class="mt-16">
        <label class="text-3xl mr-4">Original language:</label>
        <span 
          class="mr-4 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl inline-block">
          {{ movie.original_language }}
        </span>
      </div>
      
      <div class="mt-8">
        <label class="text-3xl mr-4">Spoken languages:</label>
      </div>
      <span v-for="lang in movie.spoken_languages" 
        :key="lang" 
        class="mr-4 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl inline-block">
        {{ lang }}
      </span>
      
      <div class="mt-8">
        <label class="text-3xl mr-4">Keywords:</label>
      </div>
      <span v-for="word, i in String(movie.keywords).split(' ')" 
        :key="i" 
        class="mr-4 px-4 py-1 border text-2xl rounded-full font-bold bg-green-500 shadow-xl inline-block">
        {{ word }}
      </span>
  </div>
</div>

</template>

<script>
import axios from 'axios';
import MovieTile from './MovieTile.vue';

export default {
  data() {
    return {
      movie: {}
    }
  },
  mounted() {
    this.loadMovie()
  },
  components: {
    MovieTile
  },
  props: ["id", "scoreType"],

  methods: {
    loadMovie() {
      axios.get(`http://localhost:5000/db/movie?id=${this.id}`)
        .then((response) => {
          this.movie = response.data
          console.log(this.movie)
        })
        .catch((error) => {
          console.error("Error: ", error);
        });
    },
  }
}
</script>
