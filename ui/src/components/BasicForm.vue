<template>
  <div class="container pt-32">

    <form @submit.prevent="submitForm" class="movie-form">
      <div class="form-group">
        <label for="original_language">Original Language:</label>
        <input v-model="formData.original_language" class="form-control" type="text" id="original_language" name="original_language">
      </div>
      
      <div class="form-group">
        <label for="runtime">Runtime:</label>
        <input v-model="formData.runtime" class="form-control"  type="text" id="runtime" name="runtime">
      </div>
      
      <div class="form-group">
        <label for="belongs_to_collection">Belongs to Collection:</label>
        <input v-model="formData.belongs_to_collection" class="form-control"  type="text" id="belongs_to_collection" name="belongs_to_collection">
      </div>
      
      <div class="form-group">
        <label for="release_date">Release Date:</label>
        <input v-model="formData.release_date" type="date" class="form-control" id="release_date" name="release_date">
      </div>
      
      <div class="form-group">
        <label for="genres">Genres:</label>
        <VueMultiselect
        v-model="formData.genres"
        :options="genres"
        :multiple="true"
        />
      </div>
      
      <div class="form-group">
        <label>Directors:</label>
        <VueMultiselect
        v-model="formData.directors"
        :options="people"
        :multiple="true"
        :label="'name'"
        :trackBy="'id'"
        />
      </div>
      
      <div class="form-group">
        <label>Actors:</label>
        <VueMultiselect
        v-model="formData.actors"
        :options="people"
        :multiple="true"
        :label="'name'"
        :trackBy="'id'"
        />
      </div>
      
      <div class="form-group">
        <label for="production_companies">Production Companies:</label>
        <VueMultiselect
        v-model="formData.production_companies"
        :options="production_companies"
        :multiple="true"
        />
      </div>
      
      <div class="form-group">
        <label for="spoken_languages">Spoken Languages:</label>
        <VueMultiselect
        v-model="formData.spoken_languages"
        :options="spoken_languages"
        :multiple="true"
        />
      </div>
      
      <div class="form-group">
        <label for="keywords">Keywords:</label>
        <input v-model="formData.keywords" class="form-control" type="text" id="keywords" name="keywords">
      </div>
      
      <div class="form-group">
        <label for="videos">Videos:</label>
        <input v-model="formData.videos" class="form-control" type="text" id="videos" name="videos">
      </div>
      
      <div class="form-group">
        <input class="form-control" type="submit" value="Submit">
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import VueMultiselect from 'vue-multiselect'

export default {
  data() {
    return {
      formData: {
        belongs_to_collection: "",
        genres: [],
        original_language: "", 
        release_date: "",
        production_companies: [],
        runtime: "",
        spoken_languages: [],
        status: "", 
        keywords: "",
        videos: "",
        actors: [],
        directors: []
      },
      people: [],
      genres: [],
      production_companies: [],
      spoken_languages: []

    };
  },
  components: {
    VueMultiselect 
  },
  created() {
    this.loadPeople()
    this.loadGenres()
    this.loadCompanies()
    this.loadLanguages()
  },
  methods: {
    parseDataToSubmit() {
      let parsedData = {...this.formData}
      parsedData.directors = parsedData.directors.map(director => director.id)
      parsedData.actors = parsedData.actors.map(actor => actor.id)

      return parsedData
    },

    submitForm() {
      let formData = this.parseDataToSubmit()
      const jsonData = JSON.stringify(formData);

      const headers = {
        'Content-Type': 'application/json'
      };

      console.log(jsonData);
      axios.post("http://localhost:5000/model/predict", jsonData, { headers })
      .then(response => {
        console.log("Response: ", response.data)
      })
      .catch(error => {
        console.error("Error: ", error)
      })
      // this.$emit('form-submitted', this.parseDataToSubmit());
    },
    async loadPeople() {
      axios.get("http://localhost:5000/data/people")
      .then(response => {
        this.people = response.data
        this.people = Object.entries(this.people).map(([key, value]) => ({
          id: key, name: value
        }));
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadGenres() {
      axios.get("http://localhost:5000/data/genres")
      .then(response => {
        this.genres = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadCompanies() {
      axios.get("http://localhost:5000/data/companies")
      .then(response => {
        this.production_companies = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadLanguages() {
      axios.get("http://localhost:5000/data/languages")
      .then(response => {
        this.spoken_languages = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    }
  }
};
</script>

<style scoped>
.movie-form {
  max-width: 400px;
  margin: auto;
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
}

select {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>