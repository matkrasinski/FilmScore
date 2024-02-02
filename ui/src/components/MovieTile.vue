<template>
  <div>
    <div class="flex flex-col items-center  rounded-3xl gap-16 my-16">
      <score-circle :score="this.currentMovie[this.score]" class="absolute bottom-0 right-0 score scale-35" :style="{'margin': mrg}" :bgColor="cColor"></score-circle>

      <img v-if="imagePath != null" :src="this.imagePath" class="rounded-3xl shadow-2xl">
      <div v-else class="py-72 px-40 text-center shadow-2xl text-9xl bg-slate-200 rounded-3xl">
        <i class="bi bi-image"></i>
      </div>
    </div>
    <div class="text-center">
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
  props: ["movie", "margin", "circleColor", "scoreName"],
  components: {
    ScoreCircle
  },
  data() {
    return {
      currentMovie: this.movie,
      movieImage: null,
      imagePath: null,
      mrg: this.margin,
      cColor: this.circleColor,
      score: this.scoreName
    }
  },
  mounted() {
    this.fetchMovieImage()
  },
  methods: {
    async fetchMovieImage() {
      const url = `http://localhost:5000/db/image?id=${this.currentMovie.tmdb_id}`
      axios.get(url)
      .then(response => {
        this.imagePath = response.data
      })
      .catch(error => {
        console.error('Error occurred :', error.message);
      });
    }
  }
}

</script>
<style scoped>

.score {
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