<script setup lang="ts">
import {ref} from "vue";
import api from "@/js/http/api.ts";
import {useUserStore} from "@/stores/user.ts";
import {useRouter} from "vue-router";

const username = ref('')
const password = ref('')
const passwordConfirmed = ref('')
const errorMessage  = ref('')
const user = useUserStore()
const router = useRouter()

async function handleLogin(){
  errorMessage.value = ''
  if(!username.value.trim()){
    errorMessage.value = '用户名不能为空'
  }else if(!password.value.trim()){
    errorMessage.value = '密码不能为空'
  }else if(password.value.trim() !== passwordConfirmed.value.trim()){
    errorMessage.value = '两次输入的密码不一致'
  }else{
    try{
      const res = await api.post('api/user/account/register/',{
        username:username.value,
        password:password.value,
      })
      const data = res.data
      if(data.result === 'success'){
        user.setAccessToken(data.access)
        user.setUserInfo(data)
        await router.push({
          name:'homepage-index'
        })
      }else{
        errorMessage.value = data.result 
      }
    }catch (err){
      console.log(err)
    }
  }
}

</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100">
    <div class="w-full max-w-md px-6">
      <fieldset class="fieldset bg-white rounded-2xl shadow-xl border-0 p-8">
        <form @submit.prevent="handleLogin()" class="space-y-4">
          <div>
            <label class="label text-sm font-medium text-gray-700 mb-1">用户名</label>
            <input
              v-model="username"
              type="text"
              class="input w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
              placeholder="用户名"
            />
          </div>

          <div>
            <label class="label text-sm font-medium text-gray-700 mb-1">密码</label>
            <input
              v-model="password"
              type="password"
              class="input w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
              placeholder="密码"
            />
          </div>
          <div>
            <label class="label text-sm font-medium text-gray-700 mb-1">确认密码</label>
            <input
              v-model="passwordConfirmed"
              type="password"
              class="input w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
              placeholder="确认密码"
            />
          </div>
          <p v-if="errorMessage" class="text-sm text-red-500 mt-1">
            {{ errorMessage }}
          </p>

          <button class="btn btn-primary w-full bg-blue-600 hover:bg-blue-700 border-0 rounded-lg py-3 font-semibold transition-all transform hover:scale-[1.02]">
            注册
          </button>
          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
          </div>
        </form>
        <p class="text-center text-sm text-gray-600 mt-6">
          已经拥有账号？
          <RouterLink :to="{name: 'user-account-login-index'}" class="text-blue-600 hover:text-blue-700 font-semibold hover:underline">登录</RouterLink>
        </p>
      </fieldset>
    </div>
  </div>
</template>

<style scoped>

</style>