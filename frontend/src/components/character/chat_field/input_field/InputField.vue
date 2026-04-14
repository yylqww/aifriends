<script setup lang="ts">
import SendIcon from "@/components/navbar/icons/SendIcon.vue";
import MicIcon from "@/components/navbar/icons/MicIcon.vue";
import { ref } from "vue";

const inputText = ref("")
const isRecording = ref(false)

function handleSend() {
  if (!inputText.value.trim()) return
  console.log("发送:", inputText.value)
  inputText.value = ""
}

function handleMicClick() {
  isRecording.value = !isRecording.value
}
</script>

<template>
  <div class="absolute bottom-6 left-1/2 -translate-x-1/2 w-[calc(100%-3rem)] max-w-md">
    <div class="relative group">
      <div class="relative flex items-center transition-all duration-500">
        <input
            v-model="inputText"
            @keyup.enter="handleSend"
            class="input w-full h-12 pl-5 pr-24 rounded-2xl bg-white/10 backdrop-blur-xl
                   text-white text-[13px] placeholder:text-white/30
                   border border-white/10 shadow-lg
                   focus:outline-none focus:bg-white/15 focus:border-primary/40 focus:ring-4 focus:ring-primary/10
                   transition-all duration-300"
            type="text"
            placeholder="与 AI 伙伴开启对话..."
        >

        <div class="absolute right-2.5 flex items-center gap-1.5">
          <button
            @click="handleMicClick"
            class="w-8 h-8 rounded-xl flex items-center justify-center
                   transition-all duration-300
                   hover:bg-white/10 active:scale-90"
            :class="isRecording ? 'text-red-400 bg-red-500/20 ring-1 ring-red-500/50' : 'text-white/40 hover:text-white/80'"
          >
            <MicIcon class="w-4 h-4" :class="{'animate-pulse': isRecording}" />
          </button>

          <div class="w-[1px] h-4 bg-white/10"></div>

          <button
            @click="handleSend"
            :disabled="!inputText.trim()"
            class="w-8 h-8 rounded-xl flex items-center justify-center
                   transition-all duration-300 group/send"
            :class="inputText.trim()
                    ? 'text-primary bg-primary/10 shadow-[0_0_15px_rgba(var(--p),0.2)]'
                    : 'text-white/20 cursor-not-allowed'"
          >
            <SendIcon class="w-4 h-4 transition-transform group-hover/send:translate-x-0.5 group-hover/send:-translate-y-0.5" />
          </button>
        </div>
      </div>

      <transition name="slide-up">
        <div v-if="isRecording"
             class="absolute -top-14 left-1/2 -translate-x-1/2 px-4 py-2 rounded-xl
                    bg-white/10 backdrop-blur-md border border-red-500/30
                    text-red-400 text-[11px] font-medium flex items-center gap-2 shadow-2xl">
          <div class="flex gap-0.5">
            <div class="w-1 h-3 bg-red-400 animate-[wave_1s_infinite_0s] rounded-full"></div>
            <div class="w-1 h-4 bg-red-400 animate-[wave_1s_infinite_0.2s] rounded-full"></div>
            <div class="w-1 h-2 bg-red-400 animate-[wave_1s_infinite_0.4s] rounded-full"></div>
          </div>
          REC ON
        </div>
      </transition>
    </div>
  </div>
</template>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translate(-50%, 10px);
}

@keyframes wave {
  0%, 100% { transform: scaleY(0.5); }
  50% { transform: scaleY(1.2); }
}

.input:focus::placeholder {
  opacity: 0.5;
  transition: opacity 0.3s ease;
}
</style>