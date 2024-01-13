<template>
  <div>
    <VueMultiselect
      v-model="selected"
      :options="people"
      :multiple="true"
      >
    </VueMultiselect>
  </div>
</template>
 
<script>
import VueMultiselect from 'vue-multiselect'
import axios from 'axios' 

export default {
  components: { VueMultiselect },
  data () {
    return { 
      selected: null,
      people: []
    }
  },
  created() {
    this.loadAndParseCSV()
  }, 
  methods: {
    async loadAndParseCSV() {
      axios.get("http://localhost:5000/data/people")
      .then(response => {
        console.log("Response: ", response.data)
        this.people = Object.values(response.data)
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
  },
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>