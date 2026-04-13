<script setup lang="ts">
import { ref, watch } from "vue";

const props = defineProps(['username'])
const myUsername = ref(props.username)

// 保持数据同步
watch(() => props.username, newVal => {
  myUsername.value = newVal
})

defineExpose({
  myUsername,
})
</script>

<template>
  <div class="form-control w-full group">
    <label class="label text-sm font-medium text-gray-700 mb-1.5 transition-all duration-300 group-focus-within:text-blue-600 group-focus-within:translate-x-0.5">
      用户名
    </label>

    <input
        v-model="myUsername"
        type="text"
        class="input w-full h-11 px-4 text-sm
               bg-gray-50/50 border-gray-200 rounded-lg
               focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10
               transition-all duration-300 outline-none shadow-none"
        placeholder="请输入用户名"
    />
  </div>
</template>

<style scoped>
</style>