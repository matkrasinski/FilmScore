<!-- MovieForm.vue -->
<template>
  <form @submit.prevent="submitForm" class="movie-form">
    <div class="form-group">
      <label for="belongs_to_collection">Belongs to Collection:</label>
      <input v-model="formData.belongs_to_collection" type="text" id="belongs_to_collection" name="belongs_to_collection">
    </div>

    <div class="form-group">
      <label for="genres">Genres:</label>
      <select v-model="formData.genres" multiple class="form-control" id="genres" name="genres">
        <option value="Drama">Drama</option>
        <option value="History">History</option>
      </select>
    </div>

    <div class="form-group">
      <label for="original_language">Original Language:</label>
      <input v-model="formData.original_language" type="text" id="original_language" name="original_language">
    </div>

    <div class="form-group">
      <label for="release_date">Release Date:</label>
      <input v-model="formData.release_date" type="date" class="form-control" id="release_date" name="release_date">
    </div>


    <div class="form-group">
      <label for="runtime">Runtime:</label>
      <input v-model="formData.runtime" type="text" id="runtime" name="runtime">
    </div>
    <div class="form-group">
      <label for="production_companies">Production Companies:</label>
      <select v-model="formData.production_companies" multiple class="form-control" id="production_companies" name="production_companies">
        <option value="Syncopy">Syncopy</option>
        <option value="Universal Pictures">Universal Pictures</option>
      </select>
    </div>

    <div class="form-group">
      <label for="actors">Actors:</label>
      <select v-model="formData.actors" multiple class="form-control" id="actors" name="actors">
        <option value="nm0634240">Actor 1</option>
        <option value="nm0634240">Actor 2</option>
        <option value="nm0634240">Actor 3</option>
      </select>
    </div>

    <div class="form-group">
      <label for="directors">Directors:</label>
      <select v-model="formData.directors" multiple class="form-control" id="directors" name="directors">
        <option value="nm0634240">Director 1</option>
      </select>
    </div>

    <div class="form-group">
      <label for="spoken_languages">Spoken Languages:</label>
      <select v-model="formData.spoken_languages" multiple class="form-control" id="spoken_languages" name="spoken_languages">
        <option value="English">English</option>
      </select>
    </div>

    <div class="form-group">
      <label for="keywords">Keywords:</label>
      <input v-model="formData.keywords" type="text" id="keywords" name="keywords">
    </div>

    <div class="form-group">
      <label for="videos">Videos:</label>
      <input v-model="formData.videos" type="text" id="videos" name="videos">
    </div>

    <div class="form-group">
      <input type="submit" value="Submit">
    </div>
  </form>
</template>

<script>
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
    };
  },
  methods: {
    submitForm() {
      this.$emit('form-submitted', this.formData);
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

/* Add Bootstrap styling for button */
.btn-primary {
  background-color: #007bff;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>