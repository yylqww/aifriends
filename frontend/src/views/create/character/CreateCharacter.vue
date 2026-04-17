<script setup>
import Photo from "@/views/create/character/components/Photo.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import Name from "@/views/create/character/components/Name.vue";
import {onMounted, ref, useTemplateRef} from "vue";
import { base64ToFile } from "@/js/utils/base64_to_file.ts";
import api from "@/js/http/api.ts";
import { useRouter } from "vue-router";
import { useUserStore } from "@/stores/user.ts";
import Voice from "@/views/create/character/components/Voice.vue";

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const voiceRef = useTemplateRef('voice-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')

const errorMessage = ref('')
const isSubmitting = ref(false)
const user = useUserStore()
const router = useRouter()

const voices = ref([])
const curVoiceId = ref(null)

onMounted(async () => {
  try{
    const res = await api.get('/api/create/character/voice/get_list/',{})
    const data = res.data
    if(data.result === 'success') {
      voices.value = data.voices
      curVoiceId.value = data.voices[0].id
    }
  }catch (err){
  }
})

async function handleCreate() {
  const photo = photoRef.value?.myPhoto
  const name = nameRef.value?.myName?.trim()
  const voice = voiceRef.value?.myVoice
  const profile = profileRef.value?.myProfile?.trim()
  const backgroundImage = backgroundImageRef.value?.myBackgroundImage

  errorMessage.value = ''
  if (!photo) { errorMessage.value = '头像不能为空'; return; }
  if (!name) { errorMessage.value = '名字不能为空'; return; }
  if( !voice) { errorMessage.value = '音色不能为空'; return; }
  if (!profile) { errorMessage.value = '角色介绍不能为空'; return; }
  if (!backgroundImage) { errorMessage.value = '聊天背景不能为空'; return; }

  isSubmitting.value = true
  const formData = new FormData()
  formData.append('name', name)
  formData.append('voice_id', voice)
  formData.append('profile', profile)
  formData.append('photo', base64ToFile(photo, 'photo.png'))
  formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))

  try {
    const res = await api.post('/api/create/character/create/', formData)
    if (res.data.result === 'success') {
      await router.push({ name: 'user-space-index', params: { user_id: user.id } })
    } else {
      errorMessage.value = res.data.result
    }
  } catch (err) {
    errorMessage.value = '服务器连接失败'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100 px-6 py-12">

    <div class="w-full max-w-md reveal-card">
      <fieldset class="fieldset bg-white rounded-2xl shadow-xl border-0 p-8">

        <div class="mb-6 text-center">
          <h2 class="text-xl font-bold text-gray-800 tracking-tight">创建新角色</h2>
          <div class="mt-2 flex justify-center">
            <span class="inline-block w-8 h-1 bg-blue-500 rounded-full"></span>
          </div>
        </div>

        <div class="space-y-5">
          <div class="form-group flex justify-center">
            <Photo ref="photo-ref" />
          </div>

          <div class="form-group">
            <Name ref="name-ref" />
          </div>
          <div class="form-group">
            <Voice ref="voice-ref" :voices="voices" :curVoiceId="curVoiceId" />
          </div>

          <div class="form-group">
            <Profile ref="profile-ref" />
          </div>

          <div class="form-group">
            <BackgroundImage ref="background-image-ref" />
          </div>

          <div class="h-5 text-center">
            <p v-if="errorMessage" class="text-xs text-red-500 error-shake">
              {{ errorMessage }}
            </p>
          </div>

          <div class="flex justify-center">
            <button
              @click="handleCreate"
              :disabled="isSubmitting"
              class="btn btn-accent w-20"
            >
              <span v-if="!isSubmitting">创建</span>
              <span v-else class="loading loading-spinner loading-xs"></span>
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

.error-shake {
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-3px, 0, 0); }
  40%, 60% { transform: translate3d(3px, 0, 0); }
}

.form-group:focus-within :deep(.label) {
  color: #2563eb;
  transform: translateX(4px);
  transition: all 0.3s ease;
}
</style>