<template>
    <header
        class="text-gray-100 py-4 px-6 shadow md:flex justify-between items-center nav-bar w-full z-1 mb-15 duration-300 ease-in"
        :style="{ top: navbarPosition }"
    >
        <a href="#welcome" class="flex items-center cursor-pointer">
            <span class="text-white text-xl mr-1">
                <i class="bi bi-car-front-fill"></i>
            </span>
            <h1 class="text-xl">eDrivingSchool</h1>
        </a>


        <span
            @click="menuOpen"
            class="absolute md:hidden right-6 top-4 cursor-pointer text-4xl"
        >
            <i :class="[isOpen ? 'bi bi-x' : 'bi bi-filter-left']"></i>
        </span>

        <ul
            class="md:flex md:items-center md:px-6 px-6 md:pb-0 pb-10 md:static absolute bg-gray-900 md:w-auto w-full top-14 duration-200 ease-in"
            :class="[isOpen ? 'left-0 bg-opacity-100' : 'left-[-100%] bg-opacity-0']"
        >
            <li class="md:mx-4 md:my-0 my-6" v-for="link in links" :key="link.name">
                <a :href="link.link" class="text-xl" @click="menuOpen">{{ link.name }}</a>
            </li>
        </ul>
    </header>
</template>

<script>

export default {
    name: "DefaultNavbar",
    data() {
        return {
            links: [
                { name: "aboutUs", link: "#aboutUs" },
                { name: "howToStart", link: "#howToStart" },
                { name: "prices", link: "#priceList" },
                { name: "team", link: "#team" },
                { name: "opinions", link: "#opinions"},
                { name: "contact", link: "#contact" },
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
        window.addEventListener("scroll", this.handleScroll);
    },
    methods: {
        menuOpen() {
            this.isOpen = !this.isOpen;
        },
        handleScroll() {
            const currentScrollPos = window.scrollY;
            this.isNavbarHidden = currentScrollPos > this.prevScrollPos;
            this.prevScrollPos = currentScrollPos;
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
    background: linear-gradient(to right, #00093c, #2d0b00);
}

.language-selector {
    margin-right: 10px; /* Adjust as needed */
}

</style>