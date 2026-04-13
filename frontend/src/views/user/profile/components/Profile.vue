<script setup lang="ts">

const myProfile = defineModel<string>('profile', { default: '' })

defineExpose({
  myProfile
})
</script>

<template>
  <div class="form-control w-full group">
    <label class="label text-sm font-medium text-gray-700 mb-1.5 transition-all duration-300 group-focus-within:text-blue-600 group-focus-within:translate-x-0.5">
      个人介绍
    </label>

    <textarea
      v-model="myProfile"
      class="textarea w-full h-36 p-4 text-sm leading-relaxed
             bg-gray-50/50 border-gray-200 rounded-xl
             focus:bg-white focus:border-blue-500 focus:ring-4 focus:ring-blue-500/10
             transition-all duration-300 outline-none resize-none shadow-none"
      placeholder="写一段话向大家介绍一下自己吧..."
    ></textarea>
  </div>
</template>

<style scoped>
/* 隐藏 textarea 默认可能出现的边框阴影 */
.textarea:focus {
  outline: none;
}
</style>