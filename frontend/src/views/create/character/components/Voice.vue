<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps<{
  voices?: any[],      // 传入的音色列表
  curVoiceId?: string | number | null  // 当前选中的 ID
}>()

const myVoice = ref(props.curVoiceId || '')

watch(() => props.curVoiceId, (newVal) => {
  myVoice.value = newVal || ''
})

defineExpose({
  myVoice,
})
</script>

<template>
  <div class="form-control w-full group">
    <label class="label text-sm font-medium text-gray-700 mb-1.5 transition-all duration-300 group-focus-within:text-blue-600 group-focus-within:translate-x-0.5">
      音色
    </label>

    <select
        v-model="myVoice"
        class="select w-full h-11 px-4 text-sm font-normal
               bg-gray-50/50 border-gray-200 rounded-lg
               focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10
               transition-all duration-300 outline-none shadow-none"
    >
      <option value="" disabled selected>选择一个角色的声音</option>
      <option
          v-for="voice in voices"
          :key="voice.id"
          :value="voice.id"
      >
        {{ voice.name }}
      </option>
    </select>
  </div>
</template>

<style scoped>
.select {
  border-width: 1px;
  line-height: 2.75rem;
}

.select:focus {
  outline: none;
}
</style>