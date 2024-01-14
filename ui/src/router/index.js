import { createRouter, createWebHistory } from 'vue-router';

import MoviesPanel from "../components/MoviesPanel.vue"
import BasicForm from "../components/BasicForm.vue"
import LandingPage from "../components/LandingPage.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", name: "home", component: LandingPage, props: true },
        { path: '/movies', name: "movies", component: MoviesPanel, props: true },
        { path: "/predict", name: "predict", component: BasicForm, props:true }
    ]
});

export default router;