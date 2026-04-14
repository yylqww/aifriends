<script setup>
import Message from "@/components/character/chat_field/chat_history/message/Message.vue";
import {nextTick, onBeforeUnmount, onMounted, useTemplateRef} from "vue";
import api from "@/js/http/api.ts";

const props = defineProps(['history', 'friendId', 'character'])
const emit = defineEmits(['pushFrontMessage'])
const scrollRef = useTemplateRef('scroll-ref')
const sentinelRef = useTemplateRef('sentinel-ref')
let isLoading = false
let hasMessages = true
let lastMessageId = 0

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const sentinelRect = sentinelRef.value.getBoundingClientRect()
  const scrollRect = scrollRef.value.getBoundingClientRect()
  return sentinelRect.top < scrollRect.bottom && sentinelRect.bottom > scrollRect.top
}

async function loadMore(){
  if(isLoading || !hasMessages) return
  isLoading = true

  let newMessages = []
  try{
    const res = await api.get('api/friend/message/get_history/',{
      params:{
        last_message_id: lastMessageId,
        friend_id: props.friendId,
      }
    })
    const data = res.data
    if(data.result === 'success'){
      newMessages = data.messages
    }
  }catch (err){
  }finally {
    isLoading = false

    if(newMessages.length === 0){
      hasMessages = false
    }else{
      const oldHeight = scrollRef.value.scrollHeight
      const oldTop = scrollRef.value.scrollTop

      for(const m of newMessages) {
        emit('pushFrontMessage',{
          role: 'ai',
          content: m.output,
          id: crypto.randomUUID(),
        })
        emit('pushFrontMessage',{
          role: 'user',
          content: m.user_message,
          id: crypto.randomUUID(),
        })
        lastMessageId = m.id
      }
      await nextTick()

      const newHeight = scrollRef.value.scrollHeight
      scrollRef.value.scrollTop = oldTop + newHeight - oldHeight

      if(checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await loadMore()

  observer = new IntersectionObserver(
      entries => {
        entries.forEach(entry => {
          if(entry.isIntersecting){
            loadMore()
          }
        })
      },
      {root: null, rootMargin: '2px', threshold: 0}
  )
  observer.observe(sentinelRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
})

async function scrollToBottom(){
  await nextTick()
  if (scrollRef.value) {
    scrollRef.value.scrollTop = scrollRef.value.scrollHeight
  }
}

defineExpose({
  scrollToBottom,
})
</script>

<template>
  <div
    ref="scroll-ref"
    class="absolute top-18 left-0 w-90 h-[420px] overflow-y-scroll no-scrollbar pb-4"
  >
    <div ref="sentinel-ref" class="h-2"></div>
    <Message
        v-for="message in history"
        :key="message.id"
        :message="message"
        :character="character"
    />
    </div>
</template>

<style scoped>
/* 隐藏滚动条样式保持不变 */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>