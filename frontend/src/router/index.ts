import { createRouter, createWebHistory } from 'vue-router'
import HomepageIndex from "@/views/homepage/HomepageIndex.vue";
import FriendIndex from "@/views/friend/FriendIndex.vue";
import CreateIndex from "@/views/create/CreateIndex.vue";
import NotFoundIndex from "@/views/error/NotFoundIndex.vue";
import LoginIndex from "@/views/user/account/LoginIndex.vue";
import RegisterIndex from "@/views/user/account/RegisterIndex.vue";
import SpaceIndex from "@/views/user/space/SpaceIndex.vue";
import ProfileIndex from "@/views/user/profile/ProfileIndex.vue";
import {useUserStore} from "@/stores/user.ts";
import api from "@/js/http/api.ts";
import UpdateCharacter from "@/views/create/character/UpdateCharacter.vue";


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component:HomepageIndex,
      name: 'homepage-index',
      meta:{
        needLogin: false,
      },
    },
    {
      path:'/friend/',
      component:FriendIndex,
      name: 'friend-index',
      meta:{
        needLogin: true,
      },
    },
    {
      path:'/create/',
      component:CreateIndex,
      name: 'create-index',
      meta:{
        needLogin: true,
      },
    },
    {
      path:'/create/character/update/:character_id/',
      component:UpdateCharacter,
      name: 'update-character',
      meta:{
        needLogin: true,
      },
    },
    {
      path:'/404/',
      component:NotFoundIndex,
      name: '404',
      meta:{
        needLogin: false,
      },
    },
    {
      path:'/user/account/login/',
      component:LoginIndex,
      name: 'user-account-login-index',
      meta:{
        needLogin: false,
      },
    },
    {
      path:'/user/account/register/',
      component:RegisterIndex,
      name: 'user-account-register-index',
      meta:{
        needLogin: false,
      },
    },
    {
      path:'/user/space/:user_id/',
      component:SpaceIndex,
      name: 'user-space-index',
      meta:{
        needLogin: true,
      },
    },
    {
      path:'/user/profile/',
      component:ProfileIndex,
      name: 'user-profile-index',
      meta:{
        needLogin: true,
      },
    },
    {
      path: '/:pathMatch(.*)*',
      component:NotFoundIndex,
      name: 'not-found',
      meta:{
        needLogin: false,
      },
    },
  ],
})

router.beforeEach(async (to, from) => {
  const user = useUserStore()

  // 1. 如果有 Token 但没拉取过用户信息（说明刚刷新）
  // 必须在此处拦截并把数据“救”回来
  if (user.isLogin() && !user.hasPulledUserInfo) {
    try {
      // 假设 api 已经处理好 Authorization Header
      const res = await api.get('/api/user/account/get_user_info/')
      if (res.data.result === 'success') {
        user.setUserInfo(res.data)
        user.setHasPulledUserInfo(true)
      } else {
        user.logout() // Token 可能伪造或失效
      }
    } catch (err) {
      console.error("同步用户信息失败", err)
      user.logout()
    }
  }

  // 2. 权限拦截：现在数据已经同步完了，可以放心判断了
  if (to.meta.needLogin && !user.isLogin()) {
    return { name: 'user-account-login-index' }
  }

  return true
})

export default router