<template>
  
  <div id="priceList" class="flex flex-col bg-slate-50 pt-32 shadow">
    <searching-bar/>
    <div id="con" class="container py-32">
      <button @click="prevPage" :disabled="currentPage === 0">
        <div class="bg-emerald-600 rounded-full w-24 h-24 flex items-center justify-center m-0 p-0 green-shadow">
          <i class="bi bi-chevron-left text-3xl text-white"></i>
        </div>
      </button>
      <div class="grid place-items-center w-full grid-cols-1 gap-64 md:grid-cols-2 lg:grid-cols-4 my-32 text-center">
        <movie-tile
        v-for="movie in this.movies"
        :key="movie.id"
        :movie="movie"
        :margin="'280px 80% -580px 0px'"
        :circleColor="'#1f2020'"
        :scoreName="'averageRating'"
        ></movie-tile>
      </div>
      
      <button @click="nextPage" :disabled="currentPage === maxPages">
        <div class="bg-emerald-600 rounded-full w-24 h-24 flex items-center justify-center m-0 p-0 green-shadow">
          <i class="bi bi-chevron-right text-3xl text-white"></i>
        </div>
      </button>
    </div>
  </div>
</template>

<script>
import MovieTile from './MovieTile.vue';
import SearchingBar from './SearchingBar.vue';
import axios from 'axios';

export default {
  name: 'LandingPage',
  components: {
    MovieTile,
    SearchingBar
  },
  data() {
    return {
      movies: [],
      currentPage: 0,
      pageSize: 8,
      maxPages: 1000
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
      axios
        .get(`http://localhost:5000/data/movies/pages?page=${page}&size=${this.pageSize}`)
        .then((response) => {
          this.movies = response.data;
        })
        .catch((error) => {
          console.error("Error: ", error);
        });
    },
    prevPage() {
      if (this.currentPage > 0) {
        this.currentPage--;
      }
      this.loadMovies(this.currentPage);
    },
    nextPage() {
      if (this.currentPage < this.maxPages) {
        this.currentPage++;
      }
      this.loadMovies(this.currentPage);
    },
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
