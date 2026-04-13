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
  <div v-if="!userProfile" class="flex items-center gap-6 animate-pulse">
    <div class="w-24 h-24 rounded-full bg-gray-200"></div>
    <div class="space-y-3">
      <div class="h-8 w-40 bg-gray-200 rounded"></div>
      <div class="h-4 w-60 bg-gray-200 rounded"></div>
    </div>
  </div>

  <div v-else class="flex flex-col md:flex-row items-center md:items-start gap-8">

    <div class="relative shrink-0 group">
      <div class="avatar">
        <div class="w-24 h-24 md:w-28 md:h-28 rounded-full ring-4 ring-white shadow-lg overflow-hidden bg-base-200">
          <img :src="userProfile.photo" alt="Avatar" class="object-cover w-full h-full transition-transform duration-500 group-hover:scale-110" />
        </div>
      </div>
    </div>

    <div class="flex flex-col items-center md:items-start flex-1 min-w-0 pt-1">

      <div class="flex flex-wrap items-center justify-center md:justify-start gap-3 mb-3">
        <h1 class="text-3xl md:text-4xl font-black tracking-tighter text-gray-900 custom-font">
          {{ userProfile.username }}
        </h1>

        <div class="flex items-center bg-gray-100 px-2 py-0.5 rounded border border-gray-200/60">
          <span class="text-[10px] font-mono font-bold text-gray-400 mr-1 tracking-tighter">UID</span>
          <span class="text-[11px] font-mono font-bold text-gray-600">{{ userProfile.id }}</span>
        </div>

        <div v-if="userProfile.id === 1" class="badge badge-sm bg-blue-500 text-white py-3 px-3 gap-1.5 font-bold text-[11px] border-none shadow-[0_0_15px_rgba(59,130,246,0.3)] transition-all">
          <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 20 20">
            <path d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"></path>
          </svg>
          开发者
        </div>
      </div>

      <div class="w-full max-w-xl">
        <div v-if="isEditing" class="mt-1">
          <textarea
            v-model="editedProfile"
            class="w-full p-3 text-sm bg-gray-50 border-l-4 border-blue-500 outline-none transition-all resize-none min-h-[70px]"
            maxlength="100"
            autofocus
          ></textarea>
          <div class="flex justify-end gap-4 mt-2">
            <button @click="isEditing = false" class="text-xs text-gray-400 hover:text-gray-600">取消</button>
            <button @click="handleSave" :disabled="isSaving" class="text-xs font-bold text-blue-600 border-b border-blue-200">
              {{ isSaving ? '更新中' : '保存修改' }}
            </button>
          </div>
        </div>

        <div
          v-else
          @click="userProfile.id === userStore.id && (isEditing = true)"
          class="group/profile relative inline-flex items-center"
          :class="userProfile.id === userStore.id ? 'cursor-pointer' : ''"
        >
          <p class="text-gray-500 text-sm md:text-base leading-relaxed font-medium transition-colors group-hover/profile:text-gray-800">
            {{ userProfile.profile || '这个人很懒，什么都没写。' }}
          </p>
          <span v-if="userProfile.id === userStore.id" class="ml-2 text-[10px] text-blue-400 font-bold opacity-0 group-hover/profile:opacity-100 transition-opacity">编辑</span>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* 针对中文字符的字体优化：优先使用系统默认的高级黑体 */
.custom-font {
  font-family: "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Helvetica Neue", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
}

.flex {
  animation: fadeIn 0.8s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateX(-5px); }
  to { opacity: 1; transform: translateX(0); }
}
</style>