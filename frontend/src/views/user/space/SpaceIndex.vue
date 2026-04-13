<script setup>
import UserInfo from "@/views/user/space/components/UserInfo.vue";
import {nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch} from "vue";
import api from "@/js/http/api.ts";
import {useRoute, useRouter} from "vue-router";
import {useUserStore} from "@/stores/user.ts";
import retro from "daisyui/theme/retro/index.js";
import Character from "@/components/character/Character.vue";

const userProfile = ref(null)
const characters = ref([])
const isLoading = ref(false )
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()

function checkSentinelVisible() {  // 判断哨兵是否能被看到
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
    // 只有当 ID 真的变了才刷新（防止某些情况下的重复触发）
    if (newId !== oldId) {
      // 1. 重置所有状态
      userProfile.value = null;
      characters.value = [];
      hasCharacters.value = true;
      isLoading.value = false;

      // 2. 重新加载数据
      await loadMore();
    }
  }
);

function removeCharacter(characterId){
  characters.value = characters.value.filter(c => c.id !== characterId)
}

</script>

<template>
  <div class="flex flex-col items-center mb-12 ">
    <UserInfo :userProfile="userProfile"/>
    <div class="grid grid-cols-[repeat(auto-fill,minmax(240px,1fr))] gap-16 mt-12 justify-items-center w-full px-9">
      <Character
          v-for="character in characters"
          :key="character.id"
          :character="character"
          :canEdit="true"
          @remove="removeCharacter"
      />
    </div>
    <div ref="sentinel-ref" class="h-2 mt-8 w-100" />
    <div v-if="isLoading" class="text-gray-500 mt-4">
      加载中...
    </div>
    <div v-else-if="!hasCharacters" class="text-gray-500 mt-4">
      没有更多角色了
    </div>
  </div>
</template>

<style scoped>

</style>