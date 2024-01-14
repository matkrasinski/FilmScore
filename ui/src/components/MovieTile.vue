<template>
  <div>
    <div class="flex flex-col items-center  rounded-3xl gap-16">
      <score-circle :score="prepareRating()" class="score scale-25"></score-circle>
      <div class="py-64 px-32 text-center shadow-2xl text-9xl bg-slate-200 rounded-3xl">
        <i class="bi bi-image"></i>
      </div>
      <div>
        <h1 class="font-bold text-3xl">{{ currentMovie.original_title }}</h1>
        <h2 class="text-2xl">{{ currentMovie.release_date }}</h2>
      </div>
      
    </div>

  </div>
</template>

<script>
import ScoreCircle from './ScoreCircle.vue';

export default {
  name: 'MovieTile',
  props: ["movie"],
  components: {
    ScoreCircle
  },
  data() {
    return {
      currentMovie: this.movie
    }
  },
  methods: {
    prepareRating() {
      let rating = this.currentMovie.averageRating
      rating = parseInt(rating * 1000) / 100;
      return rating
    }
  }

}

</script>
<style scoped>
.score {
    margin: 280px 60% -540px 0px;
    z-index: 1;
}
i {
  color: #363e70;
}
.scale-25 {
  --tw-scale-x: .35;
  --tw-scale-y: .35;
  transform: translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
}



</style>