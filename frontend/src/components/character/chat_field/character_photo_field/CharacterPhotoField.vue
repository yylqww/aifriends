<script setup>
defineProps(['character'])
</script>

<template>
  <div class="absolute left-6 top-6 z-20 select-none">
    <div class="flex items-center gap-2.5 pl-1.5 pr-4 py-1.5 rounded-full
                bg-white/5 backdrop-blur-xl
                border border-white/10 shadow-2xl
                transition-all duration-500 hover:bg-white/10 hover:border-white/20 group">

      <div class="w-8 h-8 rounded-full overflow-hidden ring-2 ring-white/20
                  transition-transform duration-500 group-hover:scale-110 group-hover:rotate-3">
        <img
          :src="character.photo"
          :alt="character.name"
          class="w-full h-full object-cover"
        >
      </div>

      <div class="flex flex-col gap-0">
        <span class="text-white/90 text-[13px] font-semibold tracking-wide truncate max-w-[100px]">
          {{ character.name }}
        </span>
        <div class="flex items-center gap-1">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-[9px] text-white/40 uppercase tracking-tighter font-medium">在线</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
span {
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>