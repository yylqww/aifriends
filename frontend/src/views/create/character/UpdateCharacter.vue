<script setup lang="ts">
import Photo from "@/views/create/character/components/Photo.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import Name from "@/views/create/character/components/Name.vue";
import {onMounted, ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.ts";
import api from "@/js/http/api.ts";
import {useRoute, useRouter} from "vue-router";
import {useUserStore} from "@/stores/user.ts";
import Voice from "@/views/create/character/components/Voice.vue";

interface Character {
  id: number;
  name: string;
  profile: string;
  photo: string;
  background_image: string;
  voice_id: string | number;
}

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const voiceRef = useTemplateRef('voice-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errorMessage = ref('')
const user = useUserStore()
const router = useRouter()
const route = useRoute()

const characterId = Array.isArray(route.params.character_id)
  ? route.params.character_id[0]
  : route.params.character_id

const character = ref<Character | null>(null)

const voices = ref<any[]>([])
const curVoiceId = ref<string | number | null>(null)

onMounted(async () => {
  try{
    const res = await api.get('/api/create/character/get_single/',{
      params:{
        character_id: characterId,
      }
    })
    const data = res.data
    if(data.result === 'success'){
      character.value = data.character
      voices.value = data.voices
      curVoiceId.value = data.character.voice_id
    }
  }catch (err){}
})

async function handleUpdate(){
  const photo = photoRef.value?.myPhoto
  const name = nameRef.value?.myName?.trim()
  const voice = voiceRef.value?.myVoice
  const profile = profileRef.value?.myProfile?.trim()
  const backgroundImage = backgroundImageRef.value?.myBackgroundImage

  errorMessage.value = ''
  if(!photo){
    errorMessage.value = '头像不能为空'
  }else if(!name){
    errorMessage.value = '名字不能为空'
  }else if(!voice){
    errorMessage.value = '音色不能为空'
  } else if(!profile){
    errorMessage.value = '角色介绍不能为空'
  }else if(!backgroundImage){
    errorMessage.value = '聊天背景不能为空'
  }else{
    const formData = new FormData()
    // 统一转为 String 解决 TS 报错及后端匹配问题
    formData.append('character_id', String(characterId))
    formData.append('name', name)
    formData.append('voice_id', String(voice))
    formData.append('profile', profile)

    if(photo !== character.value?.photo){
      formData.append('photo', base64ToFile(photo,'photo.png'))
    }

    if(backgroundImage !== character.value?.background_image){
      formData.append('background_image',base64ToFile(backgroundImage,'background_image.png'))
    }

    try{
      const res = await api.post('/api/create/character/update/', formData)
      const data = res.data
      if(data.result === 'success'){
        await router.push({
          name:'user-space-index',
          params:{
            user_id: user.id
          }
        })
      }else{
        errorMessage.value = data.result
      }
    }catch (err){}
  }
}
</script>

<template>
  <div v-if="character" class="flex justify-center">
    <div class="card w-120 bg-base-200 shadow-sm mt-16">
      <div class="card-body">
        <h3 class="font-bold text-lg my-4">
          更新角色
        </h3>
        <Photo ref="photo-ref" :photo="character.photo" />
        <Name ref="name-ref" :name="character.name"/>
        <Voice ref="voice-ref" :voices="voices" :curVoiceId="curVoiceId" />
        <Profile ref="profile-ref" :profile="character.profile" />
        <BackgroundImage ref="background-image-ref" :backgroundImage="character.background_image" />
        <p v-if="errorMessage" class="text-sm text-red-500">
          {{ errorMessage }}
        </p>
        <div class="flex justify-center">
          <button @click="handleUpdate" class="btn btn-accent w-20 mt-2">
            更新
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>