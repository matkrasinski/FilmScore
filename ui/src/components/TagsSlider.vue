<template>
   <div class="flex flex-col pt-16">
        <h1 class="mb-4 text-5xl font-extrabold text-gray-900 text-center py-8">Get movies by genres</h1>

          <carousel :items-to-show="this.numOfDisplayableElemets" class="mb-16">
            <slide v-for="item in genres" :key="item" class="h-full" @click="item.isClicked = !item.isClicked, this.$emit('selected-genres', genres.filter(e => e.isClicked).map(e => e.name))">
              <p class="px-4 py-1  text-2xl rounded-full font-bold shadow-2xl cursor-pointer hover:no-underline"
              :style="{ backgroundColor: item.isClicked ? '#15803d' : '#34d399'}"
              
              >
              {{ item.name }}
            </p>
          </slide>
          
          <template #addons>
            <navigation />
          </template>
        </carousel>
      
        <carousel :items-to-show="2" class="mb-16">
          <slide v-for="item in this.sortBy" :key="item" class="h-full">
            <p class="px-4 py-1 border text-2xl rounded-full font-bold bg-yellow-400 cursor-pointer hover:no-underline shadow-2xl"
            @click="handleSortClicked(item)"
            >
            {{ item.name}} 
            <i v-if="item.isClicked && item.asc" class="bi bi-caret-up-fill"></i>
            <i v-else-if="item.isClicked && !item.asc" class="bi bi-caret-down-fill"></i>
          </p>
        </slide>
      </carousel>
    </div>
</template>


<script>
import 'vue3-carousel/dist/carousel.css'
import { Carousel, Slide, Navigation } from 'vue3-carousel'

export default {
  name: 'TagsSlider',
    components: {
        Carousel,
        Slide,
        Navigation,
    },
    data() {
      return {
        genres:[
          {name: 'Mystery', isClicked: false}, {name: 'Fantasy', isClicked: false}, {name: 'Adventure', isClicked: false}, {name: 'Thriller', isClicked: false},
          {name: 'History', isClicked: false}, {name: 'Documentary', isClicked: false}, {name: 'Crime', isClicked: false}, {name: 'Comedy', isClicked: false},
          {name: 'Horror', isClicked: false} ,{name: 'Family', isClicked: false} ,{name: 'Western', isClicked: false}, {name: "Romance", isClicked: false},
          {name: 'Music', isClicked: false}, {name: 'Action', isClicked: false}, {name: 'TV Movie', isClicked: false}, {name: 'War', isClicked: false},
          {name: 'Drama', isClicked: false} ,{name: 'Animation', isClicked: false} ,{name: 'Science Fiction', isClicked: false}
        ],      
        sortBy: {
          rating: {name: "Average rating", isClicked: false, asc: false, clicks: 1},
          numberOfVotes: {name: "Number of Votes", isClicked: false, asc: false, clicks: 1}
        },
        smallWidthThreshold: 600,
        numOfDisplayableElemets: 8,
        buttonCollor: "#34d399"
      }
    },
    mounted() {
      this.updatePicture()
      window.addEventListener('resize', this.updatePicture);
    },
    methods: {        
      updatePicture() {
        const isSmallWidth = window.innerWidth <= this.smallWidthThreshold;
        this.numOfDisplayableElemets = isSmallWidth ? 3 : 10
      },
      beforeUnmount() {
        window.removeEventListener('resize', this.updatePicture);
      },
      handleSortClicked(item) {
        if (item.clicks % 3 == 0) {
          item.isClicked = !item.isClicked
          item.asc = !item.asc
          item.clicks = 0
        } else if (item.clicks % 2 == 0) {
          item.asc = !item.asc
        } else {
          item.isClicked = !item.isClicked
        }
        item.clicks++;
        this.$emit("sort-movies", this.getSortBy())
      },
      getSortBy() {
        let byRating = ""
        if (this.sortBy.rating.isClicked) {
          byRating = this.sortBy.rating.asc ? "asc" : "desc"
        }

        let byNumVotes = ""
        if (this.sortBy.numberOfVotes.isClicked) {
          byNumVotes = this.sortBy.numberOfVotes.asc ? "asc" : "desc"
        }

        return {
          "rating": byRating,
          "numVotes": byNumVotes
        }
      }



    }
}

</script>