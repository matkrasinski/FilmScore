<template>
<div class="relative z-10" aria-labelledby="modal-title" role="dialog" aria-modal="true">
  <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

  <div class="fixed inset-0 z-10 w-screen overflow-y-auto flex min-h-full items-end justify-center p-8 text-center sm:items-center">
      <div class="relative transform overflow-hidden rounded-3xl bg-white text-left shadow-xl transition-all">
        <div class=" px-4 py-3 sm:flex sm:flex-row-reverse sm:px-6">
          <i class="bi bi-x-lg text-4xl text-gray-400 cursor-pointer" @click="this.$emit('modalClosed')"></i>
        </div>
        <div class="bg-white px-24  sm:flex sm:items-start mb-64 text-center justify-center">
          <score-circle :score="this.score" class="score scale-35 shadow-2xl rounded-full" :bgColor="'black'"/>
        </div>
        <div @click="exportToJSON" class="text-center save-button rounded-r-full rounded-l-full shadow-2xl py-8 mb-8 mr-32 ml-32 cursor-pointer font-extrabold text-2xl ">
          Export to JSON
        </div>
      </div>
  </div>
</div>

</template>

<script>
import ScoreCircle from './ScoreCircle.vue';

export default {
  name: "PredictionModal",
  props: ["score", "formData"],
  components: {
    ScoreCircle
  },
  data() {
    return {
      dataToSave: this.formData
    }
  },
  methods: {
    exportToJSON() {
      this.dataToSave.prediction = this.score
      const jsonContent = JSON.stringify(this.dataToSave, null, 2);
      const blob = new Blob([jsonContent], { type: "application/json" });
      const link = document.createElement("a");
      link.setAttribute("href", URL.createObjectURL(blob));
      link.setAttribute("download", "data.json");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    },
  }
}


</script>

<style scoped>
.score {
    z-index: 1;
}
.save-button {
  background-color: #f7e018;
}

</style>


