<script setup lang="ts">
import {markRaw, ref, useTemplateRef, watch} from "vue";
import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import { useUserStore } from "@/stores/user.ts";
import UserMenu from "@/components/navbar/UserMenu.vue";
import {useRoute, useRouter} from "vue-router";

const searchInput = useTemplateRef<HTMLInputElement>('searchInput');


const user = useUserStore()
const router = useRouter()
const route = useRoute()
const searchQuery = ref(route.query.q?.toString() || '')


const menuItems = [
  { name: 'home', label: '首页', to: 'homepage-index', icon: markRaw(HomepageIcon) },
  { name: 'friend', label: '好友', to: 'friend-index', icon: markRaw(FriendIcon) },
  { name: 'create', label: '创作', to: 'create-index', icon: markRaw(CreateIcon) },
]

const moveCursorToEnd = () => {
  setTimeout(() => {
    if (searchInput.value) {
      const len = searchInput.value.value.length;
      searchInput.value.setSelectionRange(len, len);
    }
  }, 0); 
};

const handleSearch = () => {
  const text = searchQuery.value.trim();

  if (text === (route.query.q || '')) return;

  router.push({
    name: 'homepage-index',
    query: text ? { q: text } : {}
  });
};

watch(() => route.query.q, (newQ) => {
  searchQuery.value = (newQ as string) || '';
});
</script>

<template>
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />

    <div class="drawer-content flex flex-col">
      <nav class="navbar sticky top-0 z-40 w-full bg-base-100/80 backdrop-blur-md border-b border-base-content/5 px-4 h-16">
        <div class="navbar-start">
          <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost hover:bg-base-content/5 transition-colors">
            <MenuIcon class="w-5 h-5 text-base-content" />
          </label>
          <div class="px-2 font-black text-2xl tracking-tighter text-base-content select-none">
            AIFriends
          </div>
        </div>

        <div class="navbar-center hidden md:flex w-full max-w-xl">
          <div class="join w-full rounded-full shadow-sm hover:shadow-md transition-all duration-300 border border-base-content/10 overflow-hidden bg-base-200/50">
            <input
              ref="searchInput"
              @focus="moveCursorToEnd"
              v-model="searchQuery"
              @keyup.enter="handleSearch"
              class="input join-item w-full bg-transparent border-none focus:outline-none focus:bg-base-100 transition-all px-6 text-sm"
              placeholder="搜索你感兴趣的内容..."
            />

            <button
              @click="handleSearch"
              class="btn btn-neutral join-item px-8 gap-2 border-none rounded-r-full"
            >
              <SearchIcon class="w-4 h-4 text-neutral-content" />
              <span class="font-bold text-neutral-content">搜索</span>
            </button>
          </div>
        </div>

        <div class="navbar-end gap-2">
          <template v-if="user.accessToken && !user.hasPulledUserInfo">
            <div class="btn btn-ghost btn-circle">
              <span class="loading loading-spinner loading-sm opacity-30"></span>
            </div>
          </template>

          <template v-else-if="user.isLogin()">
            <RouterLink :to="{name: 'create-index'}"
                        class="btn btn-ghost btn-sm md:btn-md rounded-full gap-2 hover:bg-base-content/10 transition-all mr-2">
              <CreateIcon class="w-5 h-5" />
              <span class="hidden sm:inline font-bold">创作</span>
            </RouterLink>
            <UserMenu />
          </template>

          <template v-else>
            <RouterLink :to="{name: 'user-account-login-index'}"
                        class="btn btn-neutral btn-sm md:btn-md rounded-full px-8 shadow-lg shadow-black/5">
              登录
            </RouterLink>
          </template>
        </div>
      </nav>

      <main class="flex-grow">
        <slot />
      </main>
    </div>

    <div class="drawer-side z-50">
      <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>
      <div class="flex min-h-full flex-col bg-base-100 border-r border-base-content/5 is-drawer-close:w-16 is-drawer-open:w-60 transition-all duration-300 overflow-x-hidden">

        <ul class="menu w-full px-3 gap-1.5 grow mt-12">
          <li v-for="item in menuItems" :key="item.name">
            <RouterLink :to="{name: item.to}"
                        active-class="bg-base-content/10 text-base-content !font-bold shadow-sm"
                        class="py-3 px-4 rounded-xl hover:bg-base-content/5 transition-all group flex items-center flex-nowrap overflow-hidden h-12"
                        :data-tip="item.label">

              <div class="flex-none w-5 h-5 flex items-center justify-center">
                <component :is="item.icon" class="w-5 h-5 transition-transform group-hover:scale-110" />
              </div>

              <span class="is-drawer-close:hidden text-[15px] ml-3 tracking-wide whitespace-nowrap overflow-hidden transition-opacity duration-200">
                {{ item.label }}
              </span>
            </RouterLink>
          </li>
        </ul>

        <div class="p-4 is-drawer-close:hidden">
          <div class="bg-base-200 rounded-2xl p-4 border border-base-content/5">
            <p class="text-[10px] font-bold text-base-content/30 uppercase tracking-[0.2em]">Version 1.0.4</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 侧边栏动画曲线优化 */
.drawer-side > div {
  transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 针对 Webkit 浏览器的滚动条微调 */
::-webkit-scrollbar {
  width: 4px;
}
::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.05);
  border-radius: 10px;
}

/* 侧边栏选中的左侧装饰线 */
.menu li a.bg-base-content\/10 {
  position: relative;
}
.menu li a.bg-base-content\/10::after {
  content: "";
  position: absolute;
  left: 0;
  top: 25%;
  height: 50%;
  width: 3px;
  background: currentColor;
  border-radius: 0 4px 4px 0;
}
</style>