<script setup lang="ts">

import {useUserStore} from "@/stores/user.ts";
import UserSpaceIcon from "@/components/navbar/icons/UserSpaceIcon.vue";
import UserProfileIcon from "@/components/navbar/icons/UserProfileIcon.vue";
import UserLogoutIcon from "@/components/navbar/icons/UserLogoutIcon.vue";
import api from "@/js/http/api.ts";
import {useRouter} from "vue-router";

const user = useUserStore()
const router = useRouter()

function closeMenu() {
  const element = document.activeElement
  if (element && element instanceof HTMLElement) element.blur()
}

async function handleLogout(){
  try{
    const res = await api.post('/api/user/account/logout/')
    const data = res.data
    if(data.result === 'success'){
      user.logout()
      await router.push({
        name:'homepage-index'
      })
    }
  }catch (err){
  }
}

</script>

<template>
  <div class="dropdown dropdown-end">
    <div tabindex="0" role="button"
         class="avatar btn-circle w-9 h-9 mr-6 cursor-pointer transition-transform duration-300 hover:scale-110 active:scale-95">
      <div class="w-9 rounded-full ring-1 ring-base-content/5 ring-offset-2 ring-offset-base-100 shadow-sm">
        <img :src="user.photo" alt="用户头像">
      </div>
    </div>

    <ul tabindex="-1"
        class="dropdown-content menu bg-base-100/90 backdrop-blur-md rounded-2xl z-30 w-52 p-2 mt-4 shadow-[0_10px_40px_rgba(0,0,0,0.1)] border border-base-content/5 animate-in fade-in slide-in-from-top-2 duration-200">

      <li class="mb-2 p-2">
        <div class="flex items-center gap-3 px-2 py-1 no-underline cursor-default pointer-events-none">
          <div class="avatar">
            <div class="w-10 rounded-full ring-1 ring-primary/20">
              <img :src="user.photo" alt="">
            </div>
          </div>
          <div class="flex flex-col min-w-0">
            <span class="text-[15px] font-black truncate text-base-content/90 tracking-tight">
              {{ user.username }}
            </span>
            <span class="text-[10px] text-base-content/40 font-mono tracking-tighter uppercase">UID: {{ user.id }}</span>
          </div>
        </div>
      </li>

      <div class="divider h-[1px] my-1 opacity-40"></div> <li>
        <RouterLink @click="closeMenu()" :to="{name: 'user-space-index', params: {user_id: user.id}}"
                    class="text-xs font-bold py-3 px-4 hover:bg-primary/5 active:bg-primary/10 transition-colors">
          <UserSpaceIcon class="w-4 h-4 opacity-70" />
          个人空间
        </RouterLink>
      </li>
      <li>
        <RouterLink @click="closeMenu()" :to="{name: 'user-profile-index'}"
                    class="text-xs font-bold py-3 px-4 hover:bg-primary/5 active:bg-primary/10 transition-colors">
          <UserProfileIcon class="w-4 h-4 opacity-70" />
          编辑资料
        </RouterLink>
      </li>

      <div class="divider h-[1px] my-1 opacity-40"></div>

      <li>
        <a @click="handleLogout()"
           class="text-xs font-bold py-3 px-4 text-error/70 hover:text-error hover:bg-error/5 transition-colors">
          <UserLogoutIcon class="w-4 h-4" />
          退出登录
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
/* 关键点：引入全局 CSS 文件作为参考（不会生成重复代码） */
@reference "@/assets/main.css";

.menu li > *:not(ul):not(.menu-title):not(details):active {
  @apply bg-transparent text-primary;
}

.animate-in {
  animation: menuShow 0.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes menuShow {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>