<template>
  <div>
    <!-- <my-multi-select></my-multi-select> -->
    <basic-form @form-submitted="handleFormSubmission"/>
  </div>
</template>

<script>
import axios from "axios"
import BasicForm from './components/BasicForm.vue'
// import MyMultiSelect from './components/MyMultiSelect.vue';


export default {
  name: 'App',
  components: {
    BasicForm, 
    // MyMultiSelect
  },
  data() {
    return {
      //
    }
  },
  methods: {
    handleFormSubmission(formData) {
      this.jsonData = JSON.stringify(formData);

      const headers = {
        'Content-Type': 'application/json'
      };

      console.log(this.jsonData);
      axios.post("http://localhost:5000/model/predict", this.jsonData, { headers })
      .then(response => {
        console.log("Response: ", response.data)
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
