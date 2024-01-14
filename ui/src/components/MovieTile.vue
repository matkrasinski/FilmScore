<template>
  <div>
    <div class="flex flex-col items-center  rounded-3xl gap-16 my-16">
      <score-circle :score="prepareRating()" class="score scale-35"></score-circle>
      <img :src="this.imagePath" class="rounded-3xl shadow-2xl">
    </div>
    <div class="">
      <h1 class="font-bold text-3xl">{{ currentMovie.original_title }}</h1>
      <h2 class="text-2xl">{{ currentMovie.release_date }}</h2>
    </div>
  </div>
</template>

<script>
import ScoreCircle from './ScoreCircle.vue';
import axios from "axios"

export default {
  name: 'MovieTile',
  props: ["movie"],
  components: {
    ScoreCircle
  },
  data() {
    return {
      currentMovie: this.movie,
      movieImage: null,
      imagePath: ""
    }
  },
  mounted() {
    this.fetchMovieImage()
  },
  methods: {
    prepareRating() {
      let rating = this.currentMovie.averageRating
      rating = parseInt(rating * 1000) / 100;
      return rating
    },
    async fetchMovieImage() {
      const url = `http://localhost:5000/data/image?id=${this.currentMovie.id}`
      axios.get(url)
      .then(response => {
        this.imagePath = response.data
      })
      .catch(error => {
        console.error('Błąd podczas pobierania strony:', error.message);
      });
    }
  }
}

</script>
<style scoped>

.score {
    margin: 280px 80% -580px 0px;
    z-index: 1;
}
i {
  color: #363e70;
}
.scale-35 {
  --tw-scale-x: .35;
  --tw-scale-y: .35;
  transform: translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
}


img {
    max-width: 40vh;
    max-height: 100vh;
    display: block;
}

</style>