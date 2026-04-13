<script setup lang="ts">
import Photo from "@/views/user/profile/components/Photo.vue";
import Profile from "@/views/user/profile/components/Profile.vue";
import Username from "@/views/user/profile/components/Username.vue";
import {useUserStore} from "@/stores/user.ts";
import {ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.ts";
import api from "@/js/http/api.ts";

const user = useUserStore()

const photoRef = useTemplateRef('photo-ref')
const usernameRef = useTemplateRef('username-ref')
const profileRef = useTemplateRef('profile-ref')
const errorMessage = ref('')
const isUpdating = ref(false)

async function handleUpdate() {
  const photo = photoRef.value?.myPhoto
  const username = usernameRef.value?.myUsername?.trim()
  const profile = profileRef.value?.myProfile?.trim()

  errorMessage.value = ''
  if(!photo){
    errorMessage.value = '头像不能为空'
    return
  }
  if(!username){
    errorMessage.value = '用户名不能为空'
    return
  }
  if(!profile){
    errorMessage.value = '简介不能为空'
    return
  }

  isUpdating.value = true
  const formData = new FormData()
  formData.append('username', username)
  formData.append('profile', profile)
  if(photo !== user.photo){
    formData.append('photo', base64ToFile(photo, 'photo.png'))
  }

  try{
    const res = await api.post('api/user/profile/update/', formData)
    const data = res.data
    if(data.result === 'success'){
      user.setUserInfo(data)
    }else{
      errorMessage.value = data.result
    }
  }catch (err){
    errorMessage.value = '服务器连接失败'
  } finally {
    isUpdating.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100 px-6 py-12">

    <div class="w-full max-w-md reveal-card">
      <fieldset class="fieldset bg-white rounded-2xl shadow-xl border-0 p-8">

        <h3 class="text-lg font-bold text-gray-800 mb-8 border-b border-gray-100 pb-4">
          编辑资料
        </h3>

        <div class="space-y-6">
          <div class="form-group">
            <Photo ref="photo-ref" :photo="user.photo" />
          </div>

          <div class="form-group">
            <Username ref="username-ref" :username="user.username" />
          </div>

          <div class="form-group">
            <Profile ref="profile-ref" :profile="user.profile" />
          </div>

          <div class="h-5">
            <p v-if="errorMessage" class="text-sm text-red-500 mt-1 error-shake">
              {{ errorMessage }}
            </p>
          </div>

          <div class="flex justify-center mt-6">
            <button
              @click="handleUpdate()"
              :disabled="isUpdating"
              class="btn btn-primary relative overflow-hidden min-w-[140px] px-8 h-10 bg-blue-600 hover:bg-blue-700 border-0 rounded-lg text-sm font-semibold transition-all transform hover:scale-[1.05] active:scale-[0.95] disabled:opacity-70"
            >
              <span v-if="!isUpdating">更新资料</span>
              <span v-else class="loading loading-spinner loading-xs"></span>
              <div class="shimmer-effect"></div>
            </button>
          </div>
        </div>

      </fieldset>
    </div>
  </div>
</template>

<style scoped>
.reveal-card {
  animation: reveal 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

@keyframes reveal {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.shimmer-effect {
  position: absolute;
  top: 0; left: -100%; width: 50%; height: 100%;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.2), transparent);
  transform: skewX(-25deg); transition: 0s;
}

button:hover .shimmer-effect {
  left: 150%; transition: 0.6s;
}

.error-shake {
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

/* 核心：CSS 穿透，确保子组件里的 label 会在聚焦时变色位移 */
.form-group:focus-within :deep(.label) {
  color: #2563eb;
  transform: translateX(4px);
  transition: all 0.3s ease;
}
</style>