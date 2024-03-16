<template>
  <div class="text-center">
    <span class="text-3xl block mt-16 mb-8">

      <span class="font-bold italic">FilmScore</span> uses <span class="italic font-serif">k</span>-NN algorithm to calculate predictions for new movies.
      Used dataset was collected from:
    </span>
    <div class="mb-16">
      <a 
      :href="`https://developer.imdb.com/non-commercial-datasets`"
      class="mr-8 px-4 py-1 border text-2xl rounded-full font-bold bg-yellow-400 shadow-xl cursor-pointer hover:no-underline ">
        IMDb Non-commercial Dataset
      </a>
      <a 
      :href="`https://developer.themoviedb.org/reference/intro/getting-started`"
      class="mr-8 px-4 py-1 border text-2xl rounded-full font-bold bg-teal-400 shadow-xl cursor-pointer hover:no-underline ">
        TMDB API
      </a>
    </div>

    <h2 class="text-3xl mb-8 font-bold">
      Features used:
    </h2>
    <div class="block text-3xl mb-16 container">
      <p v-for="feature in this.features"
        :key="feature"
        class="my-4"> 
        <span class="px-4 py-1 border text-2xl rounded-full font-bold  shadow-xl hover:no-underline "
          :class="[imdbAttributes.includes(feature.name)  ? 'bg-yellow-400' : 'bg-teal-400']" >
           {{ feature.name }}
        </span>
        - {{ feature.desc }}
      </p> 
    </div>

    <div class="text-3xl container">
      <p>
        The distribution of movies 
        <span class="px-4 py-1 border text-2xl rounded-full font-bold bg-yellow-400 shadow-xl inline-block hover:no-underline ">
          average rating
        </span>
        looks very much like Gaussian distribution.
      </p> <span class="font-bold italic">FilmScore</span> uses those ratings to calculate ratings for actors, directors and production companies.</div>
    <div class="container">

      <img :src="this.avgRatingsImg" class="scale-75">
    </div>

    <div class="text-3xl mb-8 font-bold">
      The additional features extracted from Actors, Directors and Production Companies are:
    </div>
      <span class="block mb-16">
        <ul class="text-3xl">
          <li>
            Overall actors rating
          </li>
          <li>
            Overall directors rating
          </li>
          <li>
            Overall production companies rating
          </li>
        </ul>
      </span>
    <div class="text-3xl font-bold">
      All of them were calculated using the formula:
    </div>
    <div class="container">
      
      <img class="my-4 inline-block scale-110" :src="this.ratingImg"/>
      
      <p class="text-3xl">where</p>
      
      <img class="mb-8 inline-block scale-75" :src="this.scalledImg"/>

      <p class="text-3xl mb-4 font-bold">Weights values:</p>
      
      <img  class="inline-block scale-75" :src="this.weightsImg"/>
   
      <div>
        <h2 class="text-3xl mt-8 font-bold">The results resemble Gaussian-like distribution as well</h2>
        <img :src="this.avgActorsImg" class="scale-75">
        <img :src="this.avgDirectorsImg" class="scale-75">
        <img :src="this.avgCompaniesImg" class="scale-75">
      </div>

      <div>
        <h1 class="text-3xl font-bold">Example distribution of real movies that are not released yet</h1>
        <img :src="this.avgNotReleasedImg" class="scale-75">
        <p class="mb-32 text-3xl">
          Movies often end up with a rating around <span class="font-sans">6.25</span> because many lack detailed info, making prediction model give general results
        </p>
      </div>

    </div>

  </div>
</template>

<script>
import averageRatingImg from "../../public/AverageRatings.png"
import averageActorsRatingsImg from "../../public/ActorsRatings.png"
import averageDirectorsRatingsImg from "../../public/DirectorsRatings.png"
import averageCompaniesRatingsImg from "../../public/CompaniesRatings.png"
import averageNotReleaedImg from "../../public/AverageNotReleased.png"

import ratingOverallLongFormulaImg from "../../public/rating_overall_long_formula.png"
import ratingOverallShortFormulaImg from "../../public/rating_overall_short_formula.png"
import scaledFormulasImg from  "../../public/scaled_formulas.png"
import weightsImgs from "../../public/weights.png"

export default {
  data() {
    return {
      avgRatingsImg: averageRatingImg,
      avgActorsImg: averageActorsRatingsImg,
      avgDirectorsImg: averageDirectorsRatingsImg,
      avgCompaniesImg: averageCompaniesRatingsImg, 
      avgNotReleasedImg: averageNotReleaedImg,
      ratingLongImg: ratingOverallLongFormulaImg,
      ratingShortImg: ratingOverallShortFormulaImg,
      scalledImg: scaledFormulasImg,
      weightsImg: weightsImgs,
      ratingImg: null,
      features: [
        {name: "Actors", desc: "Movies are more similar if they have the same actors" },
        {name: "Directors", desc: "Movies are more similar if they have the same actors"},
        {name: "Keywords", desc: "Movies are more similar if they have some similar keywords"},
        {name: "Promotion Videos", desc: "Movies are more similar if the number of promotion videos is similar"},
        {name: "Release Date", desc: "Movies are more similar if they are not far away of each other in time too much"},
        {name: "Production Companies", desc: "Movies are more similar if they have the same production companies"},
        {name: "Duration in minutes", desc: "Movies are more similar if they duration is similar"},
        {name: "Spoken languages", desc: "Movies are more similar if they use the same languages in them"},
        {name: "Original language", desc: "Movies are more similar if they have the same original language"},
        {name: "Movie collection", desc: "Movies are more similar if they become from the same movie collection"}
      ],
      imdbAttributes: [
        "Actors", "Directors"
      ],
      smallWidthThreshold: 600
    }
  },
  methods:{
    updatePicture() {
      const isSmallWidth = window.innerWidth <= this.smallWidthThreshold;
      this.ratingImg = isSmallWidth ? ratingOverallShortFormulaImg : ratingOverallLongFormulaImg;
      return this.ratingImg;
    }
  },
  mounted() {
    this.updatePicture()
    window.addEventListener('resize', this.updatePicture);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updatePicture);
  }
}

</script>

<style scoped>
.ml-middle {
  margin-left: 25%;
}
@media only screen and (max-width: 600px) {
    .break {
      display: block;
      margin-top: 5px;
    }
  }
</style>