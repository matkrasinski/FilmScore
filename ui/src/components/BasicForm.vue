<template>
  <div class="container">

    <form @submit.prevent="submitForm" class="movie-form">
      <div class="form-group">
        <label for="original_language">Original Language:</label>
        <VueMultiselect
        v-model="formData.original_language"
        :options="original_languages"
        :multiple="false"
        />
      </div>

      <div class="form-group">
        <label for="runtime">Movie duration in minutes:</label>
        <input v-model="formData.runtime" class="form-control" type="number" min="0" oninput="validity.valid||(value='');" id="runtime" name="runtime">
      </div>

      <div class="form-group">
        <label for="belongs_to_collection">Movie collection:</label>
        <VueMultiselect
        v-model="formData.belongs_to_collection"
        :options="collections"
        :multiple="false"
        :label="'primary_name'"
        :trackBy="'collection_id'"
        />
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
        :label="'company_name'"
        :trackBy="'company_id'"
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
      <prediction-modal v-if="submitted" @modal-closed="this.submitted = !this.submitted" :score="this.prediction" :formData="formData"></prediction-modal>
      <!-- v-if="submitted"  -->
    </form>
  </div>
</template>

<script>
import axios from 'axios'
import VueMultiselect from 'vue-multiselect'
import PredictionModal from './PredictionModal.vue';

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
      spoken_languages: [],
      original_languages: [],
      collections: [],
      prediction: null,
      submitted: false,

    };
  },
  components: {
    VueMultiselect,
    PredictionModal
  },
  created() {
    this.loadOriginalLanguages()
    this.loadCollections()
    this.loadGenres()
    this.loadPeople()
    this.loadCompanies()
    this.loadLanguages()
    
  },
  methods: {
    parseDataToSubmit() {
      let parsedData = {...this.formData}
      parsedData.directors = parsedData.directors.map(director => director.id)
      parsedData.actors = parsedData.actors.map(actor => actor.id)
      parsedData.production_companies = parsedData.production_companies.map(company => parseInt(company.company_id))
      
      parsedData.belongs_to_collection = parseInt(parsedData.belongs_to_collection.collection_id) 
      
      return parsedData
    },

    submitForm() {
      let formData = this.parseDataToSubmit()
      const jsonData = JSON.stringify(formData);
      const headers = {
        'Content-Type': 'application/json'
      };

      axios.post("http://localhost:5000/model/predict", jsonData, { headers })
      .then(response => {
        console.log("Response: ", response.data)
        this.submitted = true
        this.prediction = response.data.prediction
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadPeople() {
      axios.get("http://localhost:5000/db/people")
      .then(response => {
        this.people = response.data
        this.people = Object.values(this.people).map(value => ({
          id: value.person_id, name: value.primary_name
        }));
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadGenres() {
      axios.get("http://localhost:5000/db/genres")
      .then(response => {
        this.genres = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadCompanies() {
      axios.get("http://localhost:5000/db/companies")
      .then(response => {
        this.production_companies = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadLanguages() {
      axios.get("http://localhost:5000/db/spoken_languages")
      .then(response => {
        this.spoken_languages = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadCollections() {
      axios.get("http://localhost:5000/db/collections")
      .then(response => {
        this.collections = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    async loadOriginalLanguages() {
      axios.get("http://localhost:5000/db/og_langs")
      .then(response => {
        this.original_languages = response.data
      })
      .catch(error => {
        console.error("Error: ", error)
      })
    },
    
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