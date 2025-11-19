import { createRouter, createWebHashHistory } from "vue-router";

const index = () => import("../App.vue");
const scrolling = () => import("../components/Scrolling.vue");
const upload = () => import("../components/Upload.vue");

const routes = [
  {
    path: "/",
    name: "index",
    component: index,
  },
  {
    path: "/scrolling",
    name: "Scrolling",
    component: scrolling,
  },
  {
    path: "/upload",
    name: "Upload",
    component: upload,
  },
];

export const router = createRouter({
  history: createWebHashHistory(),
  routes: routes,
});
