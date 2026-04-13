<script setup>
import UserInfo from "@/views/user/space/components/UserInfo.vue";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch} from "vue";
import api from "@/js/http/api.ts";
import {useRoute} from "vue-router";
import Character from "@/components/character/Character.vue";

const userProfile = ref(null)
const characters = ref([])
const isLoading = ref(false )
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()

function checkSentinelVisible() {
  if (!sentinelRef.value) return false
  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore(){
  if(isLoading.value || !hasCharacters.value) return
  isLoading.value = true

  let newCharacters = []
  try{
    const res = await api.get('/api/create/character/get_list/', {
      params:{
        items_count: characters.value.length,
        user_id: route.params.user_id,
      }
    })
    const data = res.data
    if(data.result === 'success'){
      userProfile.value = data.user_profile
      newCharacters = data.characters
    }
  }catch (err){
  }finally {
    isLoading.value = false
    if(newCharacters.length === 0){
      hasCharacters.value = false;
    }else{
      characters.value.push(...newCharacters)
      await nextTick()
      if(checkSentinelVisible()){
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async() => {
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
  observer.observe(sentinelRef.value )
})

onBeforeUnmount(() => {
  observer?.disconnect()
})

watch(
  () => route.params.user_id,
  async (newId, oldId) => {
    if (newId !== oldId) {
      userProfile.value = null;
      characters.value = [];
      hasCharacters.value = true;
      isLoading.value = false;
      await loadMore();
    }
  }
);

function removeCharacter(characterId){
  characters.value = characters.value.filter(c => c.id !== characterId)
}
</script>

<template>
  <div class="flex flex-col min-h-screen">

    <div class="w-full flex justify-start bg-white py-6 border-b border-gray-100 shadow-sm px-10">
      <div class="w-full">
        <UserInfo :userProfile="userProfile"/>
      </div>
    </div>

    <div class="flex flex-col items-center w-full">
      <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-16 mt-12 justify-items-center w-full px-10 max-w-[1400px]">
        <Character
            v-for="character in characters"
            :key="character.id"
            :character="character"
            :canEdit="true"
            @remove="removeCharacter"
        />
      </div>
    </div>

    <div class="flex flex-col items-center mt-12 w-full">
      <div ref="sentinel-ref" class="h-2 w-full" />
      <div v-if="isLoading" class="flex items-center gap-2 text-gray-400 mt-4">
        <span class="loading loading-spinner loading-sm"></span>
        <span>正在加载角色...</span>
      </div>
      <div v-else-if="!hasCharacters" class="text-gray-400 mt-8 mb-12 flex items-center gap-4 w-full px-20">
        <div class="h-[1px] bg-gray-100 flex-1"></div>
        <span class="text-xs tracking-widest font-medium opacity-50">没有更多角色了</span>
        <div class="h-[1px] bg-gray-100 flex-1"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>