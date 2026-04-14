<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef } from "vue";
import api from "@/js/http/api.ts";
import Character from "@/components/character/Character.vue";

const friends = ref([])
const isLoading = ref(false)
const hasFriends = ref(true) // 语义更明确：是否有更多数据
const sentinelRef = useTemplateRef('sentinel-ref')

function checkSentinelInView() {
  if (!sentinelRef.value) return false
  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight
}

async function loadMore() {
  if(isLoading.value || !hasFriends.value) return
  isLoading.value = true

  let newFriends = []
  try{
    const res = await api.get('api/friend/get_list/',{
      params:{
        items_count: friends.value.length,
      }
    })
    const data = res.data
    if(data.result === 'success'){
      newFriends = data.friends
    }
  }catch (err){
  }finally {
    isLoading.value = false
    if(newFriends.length === 0){
      hasFriends.value = false
    }else{
      friends.value.push(...newFriends)
      await nextTick()

      if(checkSentinelInView()){
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
      if (entries[0].isIntersecting) {
        loadMore()
      }
    },
    {
      root: null,
      rootMargin: '300px',
      threshold: 0
    }
  )

  if (sentinelRef.value) observer.observe(sentinelRef.value)
})

onBeforeUnmount(() => {
  if (observer) {
    observer.disconnect()
    observer = null
  }
})

function removeFriend(friendId){
  friends.value = friends.value.filter(f => f.id !== friendId)
}
</script>

<template>
  <div class="flex flex-col items-center mb-12 min-h-screen">
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-9 mt-12 justify-items-center w-full px-9">
      <Character
          v-for="friend in friends"
          :key="friend.id"
          :character="friend.character"
          :canRemoveFriend="true"
          :friendId="friend.id"
          @remove="removeFriend"
      />
    </div>

    <div ref="sentinel-ref" class="w-full h-10 flex justify-center items-center mt-8">
      <div v-if="isLoading" class="flex items-center gap-2 text-base-content/40">
        <span class="loading loading-dots loading-md"></span>
        <span class="text-xs tracking-widest uppercase">正在加载</span>
      </div>

      <div v-else-if="!hasFriends && friends.length > 0" class="text-base-content/20 text-xs uppercase tracking-[0.2em]">
        —— 没有更多聊天角色了  ——
      </div>

      <div v-else-if="!hasFriends && friends.length === 0" class="flex flex-col items-center gap-2 opacity-30 mt-20">
        <div class="i-carbon-chat-off text-4xl"></div>
        <p class="text-sm">暂无聊天角色</p>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>