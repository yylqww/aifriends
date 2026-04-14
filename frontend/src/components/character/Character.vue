<script setup>
import {ref, useTemplateRef} from "vue";
import RemoveIcon from "@/components/navbar/icons/RemoveIcon.vue";
import {useUserStore} from "@/stores/user.ts";
import UpdateIcon from "@/components/navbar/icons/UpdateIcon.vue";
import api from "@/js/http/api.ts";
import ChatField from "@/components/character/chat_field/ChatField.vue";
import {useRouter} from "vue-router";

const props = defineProps(['character', 'canEdit'])
const isHover = ref(false)
const user = useUserStore()
const emit = defineEmits(['remove'])
const router = useRouter()

async function handleRemoveCharacter(){
  // 增加二次确认，提升容错率
  if (!confirm("确定要删除这个角色吗？")) return;

  try {
    const res = await api.post('/api/create/character/remove/', {
      character_id: props.character.id,
    })

    if(res.data.result === 'success'){
      // 成功后通知父组件，父组件会通过 filter 移除数据
      emit('remove', props.character.id)
    } else {
      alert(res.data.result || "删除失败");
    }
  } catch (err) {
  }
}

const chatFieldRef = useTemplateRef('chat-field-ref')
const friend = ref(null)

async function openChatField(){
  if(!user.isLogin()) {
    await router.push({
      'name': 'user-account-login-index'
    })
  }else{
    try{
      const res = await api.post('/api/friend/get_or_create/',{
        character_id: props.character.id,
      })
      const data = res.data
      if(data.result === 'success'){
        friend.value = data.friend
        chatFieldRef.value.showModal()
      }
    }catch (err){
    }
  }
}
</script>

<template>
  <div class="group">
    <div class="cursor-pointer overflow-hidden rounded-[1.2rem] transition-all duration-700 ease-[cubic-bezier(0.23,1,0.32,1)] border border-base-content/5 bg-base-100 hover:border-primary/30 hover:-translate-y-2"
         @click="openChatField"
         @mouseover="isHover=true"
         @mouseout="isHover=false">

      <div class="w-60 h-80 relative">
        <img :src="character.background_image"
             class="w-full h-full object-cover transition-all duration-1000"
             :class="isHover ? 'scale-105 grayscale-0' : 'scale-100 grayscale-[0.2]'"
             alt="background"
             loading="lazy">

        <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-80" />

        <div v-if="canEdit && character.author.user_id === user.id"
             class="absolute right-3 top-3 z-30 transition-all duration-500"
             :class="isHover ? 'opacity-100' : 'opacity-0'">
          <div class="flex flex-col gap-1.5 p-1 rounded-lg bg-white/10 backdrop-blur-md border border-white/20">
            <RouterLink :to="{name: 'update-character', params: {character_id: character.id}}"
                        class="btn btn-square btn-xs btn-ghost text-white hover:bg-primary/40 border-none">
               <UpdateIcon class="w-3.5 h-3.5" />
            </RouterLink>
            <button @click.stop="handleRemoveCharacter"
                    class="btn btn-square btn-xs btn-ghost text-white hover:bg-error/40 border-none">
              <RemoveIcon class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div class="absolute inset-x-0 bottom-0 p-4 z-20">
          <div class="text-[9px] font-mono text-white/40 mb-1 tracking-tighter">
            NO.{{ String(character.id).padStart(4, '0') }}
          </div>

          <div class="flex items-start gap-3">  <!-- 改为 items-start，让头像和内容顶部对齐 -->
            <div class="w-10 h-10 rounded-xl overflow-hidden border border-white/30 shadow-sm transition-transform duration-500 flex-shrink-0"
                 :class="{'rotate-6': isHover}">
              <img :src="character.photo" class="w-full h-full object-cover" alt="avatar">
            </div>

            <div class="flex-1 min-w-0">  <!-- 添加 min-w-0 防止文字溢出 -->
              <h2 class="text-white font-light text-base tracking-[0.05em] truncate">
                {{ character.name }}
              </h2>
              <!-- 角色介绍 -->
              <p class="text-white/60 text-[10px] mt-1 line-clamp-2 leading-relaxed">
                {{ character.profile || '这个角色还没有介绍哦~' }}
              </p>
              <div class="w-4 h-[1px] bg-primary transition-all duration-500 mt-2" :class="isHover ? 'w-12' : 'w-4'"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <RouterLink :to="{name: 'user-space-index', params: {user_id: character.author.user_id}}"
                class="flex items-center mt-3 px-1 gap-2 group/author w-fit">
      <div class="w-5 h-5 rounded-full overflow-hidden ring-1 ring-base-content/10 group-hover/author:ring-primary transition-all">
        <img :src="character.author.photo" alt="author">
      </div>
      <span class="text-[10px] font-medium text-base-content/40 uppercase tracking-widest group-hover/author:text-primary transition-colors">
        {{ character.author.username }}
      </span>
      <div class="w-0 h-[1px] bg-base-content/10 transition-all duration-500 group-hover/author:w-8"></div>
    </RouterLink>
    <ChatField ref="chat-field-ref" :friend="friend" />
  </div>
</template>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>