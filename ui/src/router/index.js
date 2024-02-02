import { createRouter, createWebHistory } from 'vue-router';

import BasicForm from "../components/BasicForm.vue"
import LandingPage from "../components/LandingPage.vue"
import NewReleasesPage from "../components/NewReleasesPage.vue"
import DetailPage from "../components/DetailPage.vue"
import MethodologyPage from "../components/MethodologyPage.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", name: "home", component: LandingPage, props: true },
        { path: "/movies", name: "movie_details", component: DetailPage, props: route => ({id: route.query.id, scoreType: route.query.scoreType}) },
        { path: "/releases", name: "releases", component: NewReleasesPage, props: true },
        { path: "/predict", name: "predict", component: BasicForm, props:true },
        { path: "/methodology", name: "methodology", component: MethodologyPage}
    ]
});

export default router;