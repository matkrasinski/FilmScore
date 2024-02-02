<template>
<footer class=" bg-gray-900">
    <div class="max-w-2xl mx-auto text-white py-10">
        <div class="text-center">
            <h3 class="text-3xl mb-3 font-bold"> Check out IMDb and TMDB</h3>
            <div class="flex justify-center my-10">
              
              <div class="flex items-center  w-auto rounded-lg px-4 py-2 mx-2">
                <a href="https://www.imdb.com/?ref_=nv_home">
                  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/IMDB_Logo_2016.svg/2560px-IMDB_Logo_2016.svg.png" class="w-32 md:w-64">
                </a>
              </div>
              <div class="flex items-center w-auto rounded-lg px-4 py-2 mx-2">
                <a href="https://www.themoviedb.org/">
                  <img src="https://www.themoviedb.org/assets/2/v4/logos/v2/blue_square_2-d537fb228cf3ded904ef09b136fe3fec72548ebc1fea3fbbd1ad9e36364db38b.svg" class="w-32 md:w-64">
                </a>
              </div>
            </div>
        </div>
        <div class="mt-2 flex flex-col md:flex-row md:justify-between items-center text-sm text-gray-400">
            <!-- <p class="order-2 md:order-1 mt-8 md:mt-0"> &copy; Beautiful Footer, 2021. </p> -->
            <div class="order-1 md:order-2">
            </div>
        </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: "DefaultFooter"
}
</script>
<style scoped>
.scale-25 {
  --tw-scale-x: .25;
  --tw-scale-y: .25;
  transform: translate(var(--tw-translate-x), var(--tw-translate-y)) rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y)) scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
}
footer{
  background: linear-gradient(to right,#5c2ac0,  #4861be, #0a977d);
  /* background: linear-gradient(to right, #00093c, #2d0b00); */
  width: 100%;
  bottom: 0%;
}


</style>