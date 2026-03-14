import { createRouter, createWebHistory } from "vue-router";
import { useUserStore } from "../stores/user";

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/login",
      name: "Login",
      component: () => import("../views/LoginView.vue"),
      meta: { requiresAuth: false },
    },
    {
      path: "/",
      name: "Query",
      component: () => import("../views/QueryView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/history",
      name: "History",
      component: () => import("../views/HistoryView.vue"),
      meta: { requiresAuth: true },
    },
    {
      path: "/schema",
      name: "Schema",
      component: () => import("../views/SchemaView.vue"),
      meta: { requiresAuth: true },
    },
  ],
});

router.beforeEach((to) => {
  const userStore = useUserStore();
  if (to.meta.requiresAuth && !userStore.token) {
    return { name: "Login" };
  }
});

export default router;
