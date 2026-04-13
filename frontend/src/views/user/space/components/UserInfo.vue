<script setup lang="ts">
import { ref, watch } from 'vue'
import api from "@/js/http/api.ts"
import { useUserStore } from "@/stores/user.ts"

const props = defineProps<{
  userProfile: {
    id: number;
    photo: string;
    username: string;
    profile: string;
  } | null
}>()

const userStore = useUserStore()
const isEditing = ref(false)
const editedProfile = ref('')
const isSaving = ref(false)

watch(() => props.userProfile?.profile, (newVal) => {
  editedProfile.value = newVal || ''
}, { immediate: true })

const handleSave = async () => {
  if (!props.userProfile) return
  isSaving.value = true
  const formData = new FormData()
  formData.append('username', props.userProfile.username)
  formData.append('profile', editedProfile.value)

  try {
    const res = await api.post('/api/user/profile/update/', formData)
    if (res.data.result === 'success') {
      props.userProfile.profile = editedProfile.value
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
  <div v-if="!userProfile" class="flex flex-col md:flex-row items-center justify-center mt-20 w-full px-6 gap-12 animate-pulse">
    <div class="w-32 h-32 rounded-none bg-base-300 rotate-45"></div>
    <div class="flex flex-col gap-4">
      <div class="h-12 w-64 bg-base-300"></div>
      <div class="h-4 w-48 bg-base-300"></div>
    </div>
  </div>

  <div v-else class="flex justify-center w-full mt-20 mb-12 px-6">
    <div class="flex flex-col md:flex-row items-start justify-center gap-12 md:gap-24 w-full max-w-6xl">

      <div class="relative shrink-0 group">
        <div class="absolute -inset-4 border border-base-content/5 -z-10 transition-transform duration-700 group-hover:rotate-12"></div>

        <div class="avatar">
          <div class="w-32 h-32 md:w-40 md:h-40 rounded-none overflow-hidden bg-base-200 ring-1 ring-base-content/10 ring-offset-8 ring-offset-base-100 shadow-sm transition-all duration-700 group-hover:shadow-xl">
            <img :src="userProfile.photo" alt="Avatar" class="object-cover grayscale-[0.1] group-hover:grayscale-0 transition-all duration-700" />
          </div>
        </div>

        <div class="absolute -left-10 top-0 h-full flex items-center">
          <span class="rotate-180 text-[10px] font-mono text-base-content/20 uppercase tracking-[0.5em] [writing-mode:vertical-lr]">
          </span>
        </div>
      </div>

      <div class="flex flex-col items-center md:items-start text-center md:text-left flex-1 min-w-0 pt-4">

        <div class="relative mb-8">
          <h1 class="text-5xl md:text-6xl font-extralight tracking-[0.4em] text-base-content/90 leading-none uppercase">
            {{ userProfile.username }}
          </h1>
          <div class="absolute -bottom-4 left-0 w-12 h-1 bg-primary/40"></div>
        </div>

        <div class="flex items-center gap-3 mb-8 p-1.5 rounded-full bg-base-200/50 border border-base-300/50 backdrop-blur-sm shadow-inner">
          <div class="px-3 py-1 bg-base-100 text-base-content/60 rounded-full text-[10px] font-mono tracking-wider shadow-sm">
            <span class="text-primary/50 font-bold">UID</span> {{ userProfile.id }}
          </div>

          <div v-if="userProfile.id === 1" class="badge badge-sm bg-blue-500 hover:bg-blue-600 text-white py-3 gap-1.5 font-bold text-[10px] border-none shadow-[0_0_15px_rgba(59,130,246,0.4)] transition-all">
            <svg class="w-3 h-3 fill-current" viewBox="0 0 20 20">
              <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path>
            </svg>
            开发者
          </div>
        </div>

        <div class="w-full max-w-lg relative group/edit">

          <div v-if="isEditing" class="animate-in">
            <textarea
              v-model="editedProfile"
              class="w-full bg-transparent border-l-2 border-primary/30 pl-4 py-2 text-sm font-light italic leading-relaxed focus:outline-none min-h-[80px] resize-none"
              placeholder="说点什么吧..."
              autofocus
              maxlength="100"
            ></textarea>
            <div class="flex justify-end gap-6 mt-4">
              <button @click="isEditing = false" class="text-[11px] text-base-content/40 hover:text-error transition-colors">取消</button>
              <button @click="handleSave" :disabled="isSaving" class="text-[11px] font-bold text-primary border-b border-primary/20 pb-0.5">
                {{ isSaving ? '保存中' : '更新简介' }}
              </button>
            </div>
          </div>

          <div
            v-else
            @click="userProfile.id === userStore.id && (isEditing = true)"
            :class="[
              'relative transition-all duration-500',
              userProfile.id === userStore.id ? 'cursor-pointer hover:pl-2' : ''
            ]"
          >
            <p class="text-base-content/60 font-light text-base md:text-lg leading-relaxed tracking-wide italic">
              {{ userProfile.profile || '等待一段故事的开始。' }}
            </p>

            <div v-if="userProfile.id === userStore.id" class="mt-4 flex items-center gap-3 opacity-0 group-hover/edit:opacity-100 transition-opacity duration-500">
              <div class="w-12 h-[1px] bg-base-content/10"></div>
              <span class="text-[10px] tracking-[0.2em] text-base-content/30">点击编辑个人简介</span>
            </div>
          </div>
        </div>

      </div>

    </div>
  </div>
</template>

<style scoped>
/* 细腻的进入动画 */
.flex {
  animation: fadeIn 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* 针对细字体的渲染优化 */
h1 {
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

/* 禁用默认的按钮点击缩放效果，保持杂志的“静谧感” */
.btn {
  @apply transition-none;
}
</style>