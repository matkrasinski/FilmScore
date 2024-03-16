<template>
  <div class="flex flex-col bg-slate-50 pt-2 shadow">
    <searching-bar v-if="this.movies.length != 0" @search-movies="(query) => searchMovies(query)"/>
    <div class="text-center pt-32 pb-16">
      <h1 class="justify-center text-7xl font-sans tracking-wide ">Looking for a Movie?</h1>
    </div>
    <div class="border-t border-gray-300 my-2 mx-auto w-1/2"></div>
 
    <tags-slider v-if="this.movies.length != 0" class="block" @selected-genres="(genres) => searchByGenres(genres)" @sort-movies="(sortBy) => this.sortMovies(sortBy)"></tags-slider>
    <div class="border-t border-gray-300 my-2 mx-auto w-1/2 mt-32"></div>
    <div class="text-center">
      <h2  v-if="this.movies.length != 0" :key="this.currentPage" class="text-gray-500 italic">Page {{ currentPage + 1}} out of {{ Math.max(maxPages + 1, currentPage + 1)}}</h2>
    </div>
    
    <div id="con" class="container pb-32">
      <button v-if="this.movies.length != 0" @click="prevPage" :disabled="currentPage === 0">
        <div class="bg-emerald-600 rounded-full w-24 h-24 flex items-center justify-center m-0 p-0 green-shadow">
          <i class="bi bi-chevron-left text-3xl text-white"></i>
        </div>
      </button>
      <div class="grid place-items-center w-full grid-cols-1 gap-64 md:grid-cols-2 lg:grid-cols-4 my-32 text-center">
        <movie-tile
        v-for="movie in this.movies.slice(0, pageSize)"
        :key="movie.tmdb_id"
        class="cursor-pointer"
        :movie="movie"
        :margin="'280px 80% -580px 0px'"
        :circleColor="'#1f2020'"
        :scoreName="'average_rating'"
        @click="this.$router.push({ path: '/movies', query: { id: movie.tmdb_id, scoreType: 'average_rating' } });"
        ></movie-tile>
      </div>
      
      <button v-if="this.movies.length != 0" @click="nextPage" :disabled="currentPage === maxPages">
        <div class="bg-emerald-600 rounded-full w-24 h-24 flex items-center justify-center m-0 p-0 green-shadow">
          <i class="bi bi-chevron-right text-3xl text-white"></i>
        </div>
      </button>
    </div>
    <div class="border-t border-gray-300 my-2 mx-auto w-1/2"></div>
    <div v-if="this.movies.length != 0" class="text-center mb-32">
      <h2 :key="this.currentPage" class="text-gray-500 italic">Page {{ currentPage + 1}} out of {{ maxPages + 1}}</h2>
    </div>
  </div>
</template>

<script>
import MovieTile from './MovieTile.vue';
import SearchingBar from './SearchingBar.vue';
import TagsSlider from './TagsSlider.vue';
import axios from 'axios';



export default {
  name: 'LandingPage',
  components: {
    MovieTile,
    SearchingBar,
    TagsSlider
  },
  data() {
    return {
      movies: [],
      currentPage: 0,
      pageSize: 8,
      maxPages: 1000,
      query: "",
      genres: [],
      sortBy: {}
    };
  },
  computed: {
    totalPages() {
      return Math.ceil(this.movies.length / this.pageSize);
    }
  },
  mounted() {
    this.loadMovies(this.currentPage);
  },
  methods: {
    async loadMovies(page) {
      axios.post(`http://localhost:5000/db/movies/pages?page=${page}&size=${this.pageSize}&query=${this.query}`, [this.genres, this.sortBy], {
        headers: {
          'Content-Type': 'application/json',
        }
      })
        .then((response) => {
          this.movies = response.data.movies;
          this.maxPages = response.data.max_size - 1
        })
        .catch((error) => {
          console.error("Error: ", error);
        });
    },
    async prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
      }
      this.loadMovies(this.currentPage);
    },
    async nextPage() {
      if (this.currentPage < this.maxPages) {
        this.currentPage++;
      }
      this.loadMovies(this.currentPage);
    },
    searchMovies(query) {
      this.currentPage = 0
      this.query = query
      this.loadMovies(this.currentPage)
    },
    searchByGenres(genres) {
      this.genres = genres
      this.loadMovies(this.currentPage)
    },
    sortMovies(sortBy) {
      this.sortBy = sortBy
      this.loadMovies(this.currentPage)
    }
  },
};
</script>

<style scoped>
#con {
  display: flex;
  align-items: center;
  justify-content: center; 
}
.green-shadow {
  box-shadow: 0 1px 50px 0 #15803d;
}

</style>
