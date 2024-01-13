import { createRouter, createWebHistory } from 'vue-router';

import MoviesPanel from "../components/MoviesPanel.vue"
import BasicForm from "../components/BasicForm.vue"

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/", redirect: "/movies", props: true },
        { path: '/movies', component: MoviesPanel, props: true },
        { path: "/predict", component: BasicForm, props:true }
    ]
});

export default router;