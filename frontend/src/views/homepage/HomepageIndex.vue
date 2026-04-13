<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef } from "vue";
import api from "@/js/http/api.ts";
import Character from "@/components/character/Character.vue";

const characters = ref([])
const isLoading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')

function checkSentinelVisible() {
  if (!sentinelRef.value) return false
  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore() {
  if (isLoading.value || !hasCharacters.value) return
  isLoading.value = true

  let newCharacters = []
  try {
    const res = await api.get('/api/homepage/index/', {
      params: {
        items_count: characters.value.length,
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newCharacters = data.characters
    }
  } catch (err) {
    console.error("加载首页失败", err)
  } finally {
    isLoading.value = false
    if (newCharacters.length === 0) {
      hasCharacters.value = false
    } else {
      characters.value.push(...newCharacters)
      await nextTick()
      // 如果屏幕太高没撑满，自动补下一页数据
      if (checkSentinelVisible()) {
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
        if (entry.isIntersecting) {
          loadMore()
        }
      })
    },
    { root: null, rootMargin: '200px', threshold: 0 }
  )
  if (sentinelRef.value) observer.observe(sentinelRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50/30">

    <main class="w-full flex flex-col items-center pt-8 pb-20">
      <div class="grid grid-cols-[repeat(auto-fill,minmax(260px,1fr))] gap-8 justify-items-center w-full px-4 md:px-12 max-w-[1600px]">
        <Character
          v-for="character in characters"
          :key="character.id"
          :character="character"
          :canEdit="false"
          class="character-card-home"
        />
      </div>

      <footer class="flex flex-col items-center mt-16 w-full px-10">
        <div ref="sentinel-ref" class="h-4 w-full" />

        <div v-if="isLoading" class="flex items-center gap-2 text-blue-500 py-10">
          <span class="loading loading-spinner loading-md"></span>
          <span class="text-sm font-bold tracking-widest">发现更多角色中...</span>
        </div>

        <div v-else-if="!hasCharacters" class="w-full flex items-center gap-4 text-gray-300 py-10">
          <div class="h-[1px] bg-gray-200 flex-1"></div>
          <span class="text-xs font-bold uppercase tracking-[0.2em]">没有更多了</span>
          <div class="h-[1px] bg-gray-200 flex-1"></div>
        </div>
      </footer>
    </main>
  </div>
</template>

<style scoped>

.character-card-home {
  transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

.character-card-home:hover {
  transform: translateY(-4px);
}


::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}
</style>