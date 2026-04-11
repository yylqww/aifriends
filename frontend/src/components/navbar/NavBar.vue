<script setup lang="ts">
import MenuIcon from "@/components/navbar/icons/MenuIcon.vue";
import FriendIcon from "@/components/navbar/icons/FriendIcon.vue";
import RemoveIcon from "@/components/navbar/icons/RemoveIcon.vue";
import CreateIcon from "@/components/navbar/icons/CreateIcon.vue";
import HomepageIcon from "@/components/navbar/icons/HomepageIcon.vue";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue";
import {useUserStore} from "@/stores/user.ts";
import UserMenu from "@/components/navbar/UserMenu.vue";

const user = useUserStore()
</script>

<template>
  <div class="drawer lg:drawer-open">
    <input id="my-drawer-4" type="checkbox" class="drawer-toggle" />

    <div class="drawer-content">
      <nav class="navbar w-full bg-base-100 shadow-sm">
        <div class="navbar-start">
          <label for="my-drawer-4" aria-label="open sidebar" class="btn btn-square btn-ghost">
            <MenuIcon />
          </label>
          <div class="px-0 font-bold text-xl">AIFriends</div>
        </div>
        <div class="navbar-center w-full max-w-180 flex justify-center">
          <div class="join w-4/5 flex  justify-center">
            <input
              class="input border-black join-item w-full !rounded-l-full focus:outline-none focus:border-black px-6"
              placeholder="搜索你感兴趣的内容"
            />
            <button class="btn btn-neutral join-item !rounded-r-full px-8 border-black border-l-0 gap-0!">
              <SearchIcon />搜索
            </button>
          </div>
        </div>
        <div class="navbar-end">
          <template v-if="user.accessToken && !user.hasPulledUserInfo">
            <button class="btn btn-ghost">
              <span class="loading loading-spinner loading-sm"></span>
            </button>
          </template>

          <template v-else-if="user.isLogin()">
            <RouterLink :to="{name: 'create-index'}" class="btn btn-ghost mr-6">
              <CreateIcon /> 创作
            </RouterLink>
            <UserMenu />
          </template>

          <template v-else>
            <RouterLink :to="{name: 'user-account-login-index'}" class="btn btn-soft">
              登录
            </RouterLink>
          </template>
        </div>
      </nav>
      <slot />
    </div>

    <div class="drawer-side is-drawer-close:overflow-visible">
      <label for="my-drawer-4" aria-label="close sidebar" class="drawer-overlay"></label>
      <div class="flex min-h-full flex-col items-start bg-base-200 is-drawer-close:w-16 is-drawer-open:w-54">
        <ul class="menu w-full grow">
          <li>
            <RouterLink :to="{name: 'homepage-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="首页">
              <HomepageIcon />
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">首页</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{name: 'friend-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="好友">
              <FriendIcon />
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">好友</span>
            </RouterLink>
          </li>
          <li>
            <RouterLink :to="{name: 'create-index'}" active-class="menu-focus" class="is-drawer-close:tooltip is-drawer-close:tooltip-right py-3" data-tip="创作">
              <CreateIcon />
              <span class="is-drawer-close:hidden text-base ml-2 whitespace-nowrap">创作</span>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>