import { createRouter, createWebHistory } from 'vue-router';
import type {RouteRecordRaw} from "vue-router";
import AppTop from "@/views/AppTop.vue";

const routeSettings: RouteRecordRaw[] = [
  {
    path : "/",
    name : "AppTop",
    component : AppTop,
  },
  {
    path : "/member/MemberList",
    name : "MemberList",
    component : () => {
      return import("@/views/member/MemberList.vue");
    },
  },
  {
    path : "/member/detail/:id",
    props: (routes) => {
      const num = Number(routes.params.id)
      return {
        id : num
      };
    },
    name : "MemberDetail",
    component : () => {
      return import("@/views/member/MemberDetail.vue");
    },
  },
  {
    path : "/member/MemberAdd",
    name : "MemberAdd",
    component : () => {
      return import("@/views/member/MemberAdd.vue");
    },
  },
  {
    path : "/member/MemberDelete",
    name : "MemberDelete",
    component : () => {
      return import("@/views/member/MemberDelete.vue");
    },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routeSettings
});

export default router
