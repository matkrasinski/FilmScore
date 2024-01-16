<template>
  <form>
    <div class="flex container">
        <button id="dropdown-button" data-dropdown-toggle="dropdown" class="flex-shrink-0 z-2 inline-flex items-center py-2.5 px-4 text-3xl font-medium text-center text-gray-400 bg-gray-50 border border-gray-300 rounded-s-lg hover:bg-gray-200 focus:ring-4 focus:outline-none focus:ring-gray-100 rounded-l-5xl  shadow-2xl" type="button">All categories <svg class="w-2.5 h-2.5 ms-2.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
        </svg></button>
        <div id="dropdown" class="z-10 hidden bg-white divide-y rounded-lg w-44">
            <ul class="py-2 text-sm text-gray-200" aria-labelledby="dropdown-button">
            <li>
                <button type="button" class="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Mockups</button>
            </li>
            <li>
                <button type="button" class="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-200 dark:hover:text-white">Templates</button>
            </li>
            <li>
                <button type="button" class="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Design</button>
            </li>
            <li>
                <button type="button" class="inline-flex w-full px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Logos</button>
            </li>
            </ul>
        </div>
        <div class="relative w-full">
            <input type="search" id="search-dropdown" class="block p-8 w-full z-0  text-gray-100 bg-gray-50 rounded-e-lg border-s-gray-50 border-s-2 border border-gray-300 text-3xl rounded-r-5xl shadow-2xl" placeholder="Search Mockups, Logos, Design Templates..." required>
            <button type="submit" class="absolute top-0 end-0 p-8 text-sm font-medium h-full text-white bg-emerald-500 rounded-e-lg border border-emerald-500 rounded-r-5xl shadow-2xl">
                <i class="bi bi-search text-3xl"></i>
                <span class="sr-only text-xl">Search</span>
            </button>
        </div>
    </div>
  </form>
</template>

<script>
export default {
  name: 'SearchingBar',

}

</script>

<style scoped>
.rounded-r-5xl {
  border-top-right-radius: 3rem/* 24px */;
  border-bottom-right-radius: 3rem/* 24px */;
}

.rounded-l-5xl {
  border-top-left-radius: 3rem/* 24px */;
  border-bottom-left-radius: 3rem/* 24px */;
}

</style>