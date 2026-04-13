<script setup lang="ts">
import {ref} from "vue";
import {useUserStore} from "@/stores/user.ts";
import {useRouter} from "vue-router";
import api from "@/js/http/api.ts";

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const isSubmitting = ref(false) // 增加提交状态控制动画
const user = useUserStore()
const router = useRouter()

async function handleLogin(){
  errorMessage.value = ''
  if(!username.value.trim()) {
    errorMessage.value = '用户名不能为空 '
  }else if(!password.value.trim()){
    errorMessage.value = '密码不能为空'
  }else{
    isSubmitting.value = true
    try{
      const res = await api.post('/api/user/account/login/',{
        username:username.value,
        password:password.value,
      })
      const data = res.data
      if(data.result === 'success'){
        user.setAccessToken(data.access)
        user.setUserInfo(data)
        await router.push({
          name: 'homepage-index'
        })
      }else{
        errorMessage.value = data.result
      }
    }catch (err){
      errorMessage.value = '连接服务器失败'
    } finally {
      isSubmitting.value = false
    }
  }
}

</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100 px-6">
    <div class="w-full max-w-md reveal-card">
      <fieldset class="fieldset bg-white rounded-2xl shadow-xl border-0 p-8">
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div class="form-group">
            <label class="label text-sm font-medium text-gray-700 mb-1">用户名</label>
            <input
              v-model="username"
              type="text"
              class="input w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none"
              placeholder="用户名"
            />
          </div>

          <div class="form-group">
            <label class="label text-sm font-medium text-gray-700 mb-1">密码</label>
            <input
              v-model="password"
              type="password"
              class="input w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all outline-none"
              placeholder="密码"
            />
          </div>

          <div class="h-5">
            <p v-if="errorMessage" class="text-sm text-red-500 mt-1 error-shake">{{ errorMessage }}</p>
          </div>

          <div class="flex justify-center mt-6"> <button
              :disabled="isSubmitting"
              class="btn btn-primary relative overflow-hidden min-w-[140px] px-8 h-10 bg-blue-600 hover:bg-blue-700 border-0 rounded-lg text-sm font-semibold transition-all transform hover:scale-[1.05] active:scale-[0.95] disabled:opacity-70"
            >
              <span v-if="!isSubmitting">登录</span>
              <span v-else class="loading loading-spinner loading-xs"></span>

              <div class="shimmer-effect"></div>
            </button>
          </div>

          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-200"></div>
            </div>
          </div>
        </form>

        <p class="text-center text-sm text-gray-600 mt-6">
          还没有账号？
          <RouterLink :to="{name: 'user-account-register-index'}" class="text-blue-600 hover:text-blue-700 font-semibold hover:underline">立即注册</RouterLink>
        </p>
      </fieldset>
    </div>
  </div>
</template>

<style scoped>
/* 1. 卡片入场动画：从下方20px平滑升起并淡入 */
.reveal-card {
  animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes reveal {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 2. 按钮流光动画：鼠标悬停时划过一道白光 */
.shimmer-effect {
  position: absolute;
  top: 0;
  left: -100%;
  width: 50%;
  height: 100%;
  background: linear-gradient(
    to right,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transform: skewX(-25deg);
  transition: 0s;
}

button:hover .shimmer-effect {
  left: 150%;
  transition: 0.6s;
}

/* 3. 错误信息震动效果 */
.error-shake {
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

/* 4. 输入框表单组在聚焦时 label 轻微位移反馈 */
.form-group:focus-within label {
  color: #2563eb; /* 对应 blue-600 */
  transform: translateX(2px);
  transition: all 0.3s ease;
}
</style>