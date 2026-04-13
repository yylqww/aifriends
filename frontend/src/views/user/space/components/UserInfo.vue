<script setup lang="ts">
import { ref, watch } from 'vue'
import api from "@/js/http/api.ts"
import { useUserStore } from "@/stores/user.ts"

// 1. 定义 Props
const props = defineProps<{
  userProfile: {
    id: number;
    photo: string;
    username: string;
    profile: string;
  } | null
}>()

// 2. 状态管理
const userStore = useUserStore()
const isEditing = ref(false)
const editedProfile = ref('')
const isSaving = ref(false)

// 3. 监听数据同步
watch(() => props.userProfile?.profile, (newVal) => {
  editedProfile.value = newVal || ''
}, { immediate: true })

// 4. 保存逻辑
const handleSave = async () => {
  if (!props.userProfile) return
  isSaving.value = true

  const formData = new FormData()
  formData.append('username', props.userProfile.username)
  formData.append('profile', editedProfile.value)

  try {
    const res = await api.post('/api/user/profile/update/', formData)
    if (res.data.result === 'success') {
      // 更新本地显示
      props.userProfile.profile = editedProfile.value
      // 同步全局 Store
      userStore.setUserInfo(res.data)
      isEditing.value = false
    }
  } catch (err) {
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div v-if="!userProfile" class="flex flex-col items-center justify-center mt-12 w-full animate-pulse">
    <div class="w-32 h-32 md:w-40 md:h-40 rounded-full bg-base-300 mb-6"></div>
    <div class="h-8 w-48 bg-base-300 rounded mb-4"></div>
    <div class="h-4 w-64 bg-base-200 rounded"></div>
  </div>

  <div v-else class="flex flex-col items-center justify-center mt-12 w-full max-w-4xl px-6 text-center">

    <div class="avatar mb-6">
      <div class="w-32 h-32 md:w-40 md:h-40 rounded-full ring ring-primary ring-offset-base-100 ring-offset-4 shadow-2xl transition-transform hover:scale-105 duration-300">
        <img :src="userProfile.photo" alt="用户头像" />
      </div>
    </div>

    <h1 class="text-3xl md:text-3xl font-extralight tracking-[0.2em] mb-4 text-base-content/90 uppercase">
      {{ userProfile.username }}
    </h1>

    <div class="flex items-center gap-3 mb-6">
      <div class="px-2.5 py-0.5 bg-base-200 text-base-content/50 rounded-full text-[11px] font-mono border border-base-300 shadow-sm">
        UID: {{ userProfile.id }}
      </div>
      <div v-if="userProfile.id === 1" class="badge badge-sm badge-primary py-2.5 gap-1 font-bold text-[10px]">
        <svg class="w-3 h-3 fill-current" viewBox="0 0 20 20"><path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path></svg>
        已认证开发者
      </div>
    </div>

    <div class="w-full max-w-lg relative group">

      <div v-if="isEditing" class="flex flex-col gap-2 p-2 rounded-xl bg-base-100 border border-primary/20 shadow-sm transition-all w-full max-w-sm mx-auto">
        <textarea
          v-model="editedProfile"
          class="textarea textarea-ghost w-full p-1 text-center text-sm font-light italic leading-snug focus:bg-transparent min-h-[60px] resize-none focus:outline-none text-base-content"
          placeholder="点击输入简介..."
          autofocus
          maxlength="100"
        ></textarea>

        <div class="flex items-center justify-between border-t border-base-200/60 pt-2 px-1">
          <span class="text-[9px] text-base-content/30 font-mono tracking-tighter">
            {{ editedProfile.length }} / 100
          </span>

          <div class="flex gap-1.5">
            <button @click="isEditing = false" class="btn btn-ghost btn-xs h-6 min-h-0 text-[10px] font-normal">取消</button>
            <button @click="handleSave" :disabled="isSaving" class="btn btn-primary btn-xs h-6 min-h-0 text-[10px] px-3 shadow-sm">
              <span v-if="isSaving" class="loading loading-spinner loading-[10px]"></span>
              保存
            </button>
          </div>
        </div>
      </div>

      <div
        v-else
        @click="userProfile.id === userStore.id && (isEditing = true)"
        :class="[
          'p-4 rounded-2xl transition-all duration-300 group/text relative',
          userProfile.id === userStore.id ? 'hover:bg-base-200/60 cursor-pointer' : ''
        ]"
      >
        <p class="text-base-content/70 italic text-sm md:text-base leading-relaxed break-all">
          {{ userProfile.profile || '暂无简介' }}

          <span v-if="userProfile.id === userStore.id" class="inline-flex items-center ml-2 opacity-0 group-hover/text:opacity-100 transition-opacity">
            <svg class="flex justify-center w-0 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
            </svg>
          </span>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.animate-in {
  animation: fadeInZoom 0.2s ease-out;
}
@keyframes fadeInZoom {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>