<script setup>
import { ref, useTemplateRef, onUnmounted } from "vue";
import streamApi from "@/js/http/streamApi.js";
import SendIcon from "@/components/navbar/icons/SendIcon.vue";
import MicIcon from "@/components/navbar/icons/MicIcon.vue";
import Microphone from "@/components/character/chat_field/input_field/Microphone.vue";

const props = defineProps(['friendId'])
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])
const inputRef = useTemplateRef('input-ref')
const message = ref('')

const showMic = ref(false)
let abortActiveRequest = null
let processId = 0
let mediaSource = null;
let sourceBuffer = null;
let audioPlayer = new Audio();
let audioQueue = [];
let isUpdating = false;

// --- 逻辑部分：保持原样 ---
const initAudioStream = () => {
    stopAudio();
    audioQueue = [];
    isUpdating = false;
    mediaSource = new MediaSource();
    audioPlayer.src = URL.createObjectURL(mediaSource);
    mediaSource.addEventListener('sourceopen', () => {
        try {
            sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
            sourceBuffer.addEventListener('updateend', () => {
                isUpdating = false;
                processQueue();
            });
        } catch (e) {
            console.error(e);
        }
    });
    audioPlayer.play().catch(() => {});
};

const processQueue = () => {
    if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating || mediaSource?.readyState !== 'open') {
        return;
    }
    isUpdating = true;
    const chunk = audioQueue.shift();
    try {
        sourceBuffer.appendBuffer(chunk);
    } catch (e) {
        isUpdating = false;
    }
};

const stopAudio = () => {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;
    if (mediaSource) {
        if (mediaSource.readyState === 'open') {
            try {
                mediaSource.endOfStream();
            } catch (e) {}
        }
        mediaSource = null;
    }
    if (audioPlayer.src) {
        URL.revokeObjectURL(audioPlayer.src);
        audioPlayer.src = '';
    }
};

const handleAudioChunk = (base64Data) => {
    try {
        const binaryString = atob(base64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }
        audioQueue.push(bytes);
        processQueue();
    } catch (e) {}
};

function focus() {
  inputRef.value?.focus()
}

async function handleSend(event, audio_msg) {
  let content = audio_msg ? audio_msg.trim() : message.value.trim();
  if (!content) return;

  if (abortActiveRequest) {
    abortActiveRequest();
    abortActiveRequest = null;
  }
  stopAudio();

  initAudioStream();
  const curId = ++processId;
  message.value = '';

  emit('pushBackMessage', { role: 'user', content: content, id: crypto.randomUUID() });
  emit('pushBackMessage', { role: 'ai', content: '', id: crypto.randomUUID() });

  try {
    abortActiveRequest = await streamApi('/api/friend/message/chat/', {
      body: {
        friend_id: props.friendId,
        message: content,
      },
      onmessage(data, isDone) {
        if (curId !== processId) return;
        if (data.content) {
          emit('addToLastMessage', data.content);
        }
        if (data.audio) {
          handleAudioChunk(data.audio);
        }
        if (isDone) {
          abortActiveRequest = null;
        }
      },
      onerror() {
        abortActiveRequest = null;
      },
      onclose() {
        abortActiveRequest = null;
      }
    });
  } catch (err) {
    abortActiveRequest = null;
  }
}

function handleStop() {
  ++processId;
  stopAudio();
  if (abortActiveRequest) {
    abortActiveRequest();
    abortActiveRequest = null;
  }
}

function close() {
  ++processId;
  showMic.value = false;
  stopAudio();
  if (abortActiveRequest) {
    abortActiveRequest();
    abortActiveRequest = null;
  }
}

onUnmounted(() => {
  ++processId;
  stopAudio();
  if (abortActiveRequest) {
    abortActiveRequest();
  }
});

defineExpose({
  focus,
  close,
})
</script>

<template>
  <div class="fixed bottom-6 left-0 w-full flex justify-center px-4 pointer-events-none">
    <form
      v-if="!showMic"
      @submit.prevent="handleSend"
      class="pointer-events-auto relative flex items-center w-full max-w-lg h-14 group transition-all duration-300"
    >
      <input
        ref="input-ref"
        v-model="message"
        class="w-full h-full bg-black/40 backdrop-blur-xl text-white text-base rounded-2xl px-5 pr-24 border border-white/10 outline-none focus:border-white/30 focus:ring-4 focus:ring-white/5 transition-all placeholder:text-white/30 shadow-2xl"
        type="text"
        placeholder="输入消息..."
      >

      <div class="absolute right-2 flex items-center space-x-1">
        <div
          @click="showMic = true"
          class="w-10 h-10 flex justify-center items-center rounded-xl cursor-pointer text-white/60 hover:text-white hover:bg-white/10 active:scale-90 transition-all"
        >
          <MicIcon class="w-6 h-6" />
        </div>

        <button
          type="submit"
          :disabled="!message.trim()"
          class="w-10 h-10 flex justify-center items-center rounded-xl bg-white/10 text-white hover:bg-white/20 active:scale-90 transition-all disabled:opacity-30 disabled:cursor-not-allowed disabled:active:scale-100"
        >
          <SendIcon class="w-5 h-5" />
        </button>
      </div>
    </form>

    <Microphone
        v-else
        class="pointer-events-auto shadow-2xl scale-105"
        @close="showMic = false"
        @send="handleSend"
        @stop="handleStop"
    />
  </div>
</template>

<style scoped>
/* 针对 Webkit 内核的输入框平滑处理 */
input {
  -webkit-appearance: none;
}

/* 简单的进入动画 */
form {
  animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>