<script setup>
import { ref, useTemplateRef, onUnmounted } from "vue";
import streamApi from "@/js/http/streamApi.js";
import SendIcon from "@/components/navbar/icons/SendIcon.vue";
import MicIcon from "@/components/navbar/icons/MicIcon.vue";

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')


let abortActiveRequest = null
let processId = 0

function focus() {
  inputRef.value.focus()
}

async function handleSend() {
  const content = message.value.trim()
  if (!content) return

  if (abortActiveRequest) {
    abortActiveRequest()
    abortActiveRequest = null
  }

  const curId = ++processId
  message.value = ''

  emit('pushBackMessage', { role: 'user', content: content, id: crypto.randomUUID() })
  emit('pushBackMessage', { role: 'ai', content: '', id: crypto.randomUUID() })

  try {
    abortActiveRequest = await streamApi('/api/friend/message/chat/', {
      body: {
        friend_id: props.friendId,
        message: content,
      },
      onmessage(data, isDone) {
        if (curId !== processId) return

        if (data.content) {
          emit('addToLastMessage', data.content)
        }

        if (isDone) {
          abortActiveRequest = null
        }
      },
      onerror(err) {

        abortActiveRequest = null
        console.error("Stream error:", err)
      },
      onclose() {
        abortActiveRequest = null
      }
    })
  } catch (err) {
    abortActiveRequest = null
  }
}

onUnmounted(() => {
  if (abortActiveRequest) {
    abortActiveRequest()
  }
})

defineExpose({
  focus,
})
</script>

<template>
  <form @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
    <input
        ref="input-ref"
        v-model="message"
        class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl pr-20"
        type="text"
        placeholder="文本输入..."
    >
    <div @click="handleSend" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
      <SendIcon />
    </div>
    <div class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer">
      <MicIcon />
    </div>
  </form>
</template>

<style scoped>
</style>