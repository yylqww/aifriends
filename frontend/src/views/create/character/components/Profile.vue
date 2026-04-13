<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  profile?: string
}>()

const myProfile = ref(props.profile || '')

watch(() => props.profile, (newVal) => {
  myProfile.value = newVal || ''
})


defineExpose({
  myProfile,
})
</script>

<template>
  <div class="form-control w-full group">
    <label class="label text-sm font-medium text-gray-700 mb-1.5 transition-all duration-300 group-focus-within:text-blue-600 group-focus-within:translate-x-0.5">
      角色介绍
    </label>

    <textarea
      v-model="myProfile"
      class="textarea w-full h-36 p-4 text-sm leading-relaxed
             bg-gray-50/50 border-gray-200 rounded-xl
             focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10
             transition-all duration-300 outline-none resize-none shadow-none"
    ></textarea>

  </div>
</template>

<style scoped>

textarea::-webkit-scrollbar {
  width: 5px;
}
textarea::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 10px;
}
textarea::-webkit-scrollbar-track {
  background: transparent;
}
</style>