<template>
    <div class="pt-32 bg-slate-50 z-10">
        <header
        class="text-gray-100 py-8 shadow md:flex justify-between items-center nav-bar w-full z-1 mb-15 duration-300 ease-in"
        :style="{ top: navbarPosition }"
        >
        <div @click="this.$router.push('/')" class="flex items-center">
            <span class="text-white text-xl mr-1">
            </span>
            <h1 class="text-5xl font-bold ml-4 z-20 cursor-pointer"><i class="bi bi-camera-reels-fill"></i>FilmScore</h1>
        </div>
        <span
            class="absolute md:hidden right-6 top-4 cursor-pointer text-7xl">
         <i @click="menuOpen()" :class="[isOpen ? 'bi bi-x' : 'bi bi-filter-left']"></i>
        </span>
        <ul
            class="md:flex md:items-center px-6 md:pb-0 pb-10 md:static absolute  md:w-auto w-full top-14 duration-200 ease-in"
            :class="[isOpen ? 'left-0  bg-opacity-100 py-8 my-12 bg-gray-900' : 'left-[-100%] bg-opacity-0']">
            <li class="md:mx-4 md:my-0 my-5" v-for="link in links" :key="link.name">
                <button @click="this.$router.push(link.link)" class="text-3xl font-bold">{{ link.name }}</button>
            </li>
        </ul>
    </header>
    </div>
</template>

<script>

export default {
    name: "DefaultNavbar",
    data() {
        return {
            links: [
                { name: "Home", link: "/" },
                { name: "New Releases", link: "/releases" },
                { name: "Predict", link: "/predict" },
                { name: "Methodology", link: "/methodology" },
            ],
            isOpen: false,
            isNavbarHidden: false,
            prevScrollPos: 0
        };
    },
    computed: {
        navbarPosition() {
            return this.isNavbarHidden ? "-100px" : "0";
        },
    },
    mounted() {
        window.addEventListener("scroll", this.handleScroll, { passive: true });
    },
    methods: {
        menuOpen() {
            this.isOpen = !this.isOpen;
        },
        handleScroll() {
            const currentScrollPos = window.scrollY;
            this.isNavbarHidden = currentScrollPos > this.prevScrollPos;
            this.prevScrollPos = currentScrollPos;
        },
        goTo(path) {
            this.isOpen = !this.isOpen
            this.$router.push(path)
        }
    },
    beforeUnmount() {
        window.removeEventListener("scroll", this.handleScroll);
    },
};
</script>

<style scoped>
.nav-bar {
    position: fixed;
    z-index: inherit;
    /* background: linear-gradient(to right, #1e3d61,#3e7acd,  #a5a8df, #a48fd9, #0a977d, #dffad8); */
    background: linear-gradient(to right, #00093c, #2d0b00);
    /* background: linear-gradient(to right,#5c2ac0,  #4861be, #0a977d); */
}
div {
    z-index: 10;
}

</style>