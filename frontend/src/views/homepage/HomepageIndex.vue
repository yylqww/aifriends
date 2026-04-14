<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref, useTemplateRef, watch } from "vue";
import api from "@/js/http/api.ts";
import Character from "@/components/character/Character.vue";
import { useRoute, useRouter } from "vue-router";
import SearchIcon from "@/components/navbar/icons/SearchIcon.vue"; // 确保有这个图标组件

const characters = ref([])
const isLoading = ref(false)
const hasCharacters = ref(true)
const sentinelRef = useTemplateRef('sentinel-ref')
const route = useRoute()
const router = useRouter()


function checkSentinelVisible() {
  if (!sentinelRef.value) return false
  const rect = sentinelRef.value.getBoundingClientRect()
  return rect.top < window.innerHeight && rect.bottom > 0
}

async function loadMore() {
  if (isLoading.value || !hasCharacters.value) return
  isLoading.value = true

  const searchTermAtRequest = route.query.q || ''

  let newCharacters = []
  try {
    const res = await api.get('/api/homepage/index/', {
      params: {
        items_count: characters.value.length,
        search_query: searchTermAtRequest,
      }
    })

    // 如果请求回来时，URL 上的关键词已经变了，直接抛弃结果
    if ((route.query.q || '') !== searchTermAtRequest) return

    const data = res.data
    if (data.result === 'success') {
      newCharacters = data.characters
    }
  } catch (err) {
    console.error("加载首页失败", err)
  } finally {
    // 只有当搜索词没变时才更新状态
    if ((route.query.q || '') === searchTermAtRequest) {
      isLoading.value = false
      if (newCharacters.length === 0) {
        hasCharacters.value = false
      } else {
        characters.value.push(...newCharacters)
        await nextTick()
        if (checkSentinelVisible()) {
          await loadMore()
        }
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

function reset(){
  characters.value = []
  isLoading.value = false
  hasCharacters.value = true
  loadMore()
}

// 快速清除搜索
function clearSearch() {
  router.push({ name: 'homepage-index' })
}

watch(() => route.query.q, () => {
  reset()
})

onBeforeUnmount(() => {
  observer?.disconnect()
})
</script>

<template>
  <div class="min-h-screen bg-gray-50/30">
    <main class="w-full flex flex-col items-center pt-8 pb-20">

      <div v-if="characters.length > 0" class="grid grid-cols-[repeat(auto-fill,minmax(260px,1fr))] gap-8 justify-items-center w-full px-4 md:px-12 max-w-[1600px]">
        <Character
          v-for="character in characters"
          :key="character.id"
          :character="character"
          :canEdit="false"
          class="character-card-home"
        />
      </div>

      <div v-else-if="!isLoading && characters.length === 0" class="flex flex-col items-center justify-center py-32 text-center animate-in fade-in zoom-in duration-300">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mb-6">
          <SearchIcon class="w-10 h-10 text-gray-300" />
        </div>
        <h3 class="text-xl font-black text-gray-900 tracking-tight">没找到相关角色</h3>
        <p class="text-gray-500 mt-2 max-w-[280px]">换个关键词试试，或者看看有没有打错字</p>
        <button
          @click="clearSearch"
          class="mt-8 btn btn-neutral btn-sm rounded-full px-8 shadow-lg shadow-black/5 hover:scale-105 transition-transform"
        >
          查看全部角色
        </button>
      </div>

      <footer class="flex flex-col items-center mt-16 w-full px-10">
        <div ref="sentinel-ref" class="h-4 w-full" />

        <div v-if="isLoading" class="flex items-center gap-2 text-blue-500 py-10">
          <span class="loading loading-spinner loading-md"></span>
          <span class="text-sm font-bold tracking-widest">发现更多角色中...</span>
        </div>

        <div v-else-if="!hasCharacters && characters.length > 0" class="w-full flex items-center gap-4 text-gray-300 py-10">
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

.animate-in {
  animation: fadeIn 0.5s ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}

::-webkit-scrollbar {
  width: 6px;
}
::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}
</style>