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
  <form v-if="!showMic" @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
    <input
        ref="input-ref"
        v-model="message"
        class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl pr-20"
        type="text"
        placeholder="文本输入..."
    >
    <div @click="handleSend" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
      <SendIcon />
    </div>
    <div @click="showMic = true" class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer">
      <MicIcon />
    </div>
  </form>
  <Microphone
      v-else
      @close="showMic = false"
      @send="handleSend"
      @stop="handleStop"
  />
</template>

<style scoped>
</style>