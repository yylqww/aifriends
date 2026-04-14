<script setup>
import {computed, nextTick, ref, useTemplateRef} from "vue";
import InputField from "@/components/character/chat_field/input_field/InputField.vue";
import CharacterPhotoField from "@/components/character/chat_field/character_photo_field/CharacterPhotoField.vue";
import ChatHistory from "@/components/character/chat_field/chat_history/ChatHistory.vue";

const props = defineProps(['friend'])
const modalRef = useTemplateRef('modal-ref')
const inputRef = useTemplateRef('input-ref')
const chatHistoryRef = useTemplateRef('chat-history-ref')
const history = ref([])

async function showModal(){
  modalRef.value.showModal()

  await nextTick()
  if (inputRef.value && typeof inputRef.value.focus === 'function') {
    setTimeout(() => {
      inputRef.value.focus()
    }, 50)
  }
}

function handlePushBackMessage(msg){
  history.value.push(msg)
  chatHistoryRef.value.scrollToBottom()
}

function handleAddToLastMessage(delta){
  history.value.at(-1).content += delta
  chatHistoryRef.value.scrollToBottom()
}

function handlePushFrontMessage(msg){
  history.value.unshift(msg)
}

defineExpose({
  showModal,
})

const modalStyle =  computed(() => {
  if (props.friend) {
    return {
      backgroundImage: `url(${props.friend.character.background_image})`,
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundRepeat: 'no-repeat',
    }
  } else {
    return {}
  }
})
</script>

<template>
  <dialog ref="modal-ref" class="modal">
    <div class="modal-box w-90 h-150 relative" :style="modalStyle">
      <button @click="modalRef?.close()"
              class="btn btn-sm btn-circle absolute right-2 top-2 z-50
                     bg-black/20 hover:bg-red-500/80 border-none
                     text-white/70 hover:text-white transition-all backdrop-blur-md">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
      <ChatHistory
          v-if="friend"
          ref="chat-history-ref"
          :history="history"
          :friendId="friend.id"
          :character="friend.character"
          @pushFrontMessage="handlePushFrontMessage"
      />
      <InputField
          v-if="friend"
          ref="input-ref"
          :friendId="friend.id"
          @pushBackMessage="handlePushBackMessage"
          @addToLastMessage="handleAddToLastMessage"
      />
      <CharacterPhotoField v-if="friend" :character="friend.character" />
    </div>
  </dialog>
</template>

<style scoped>

</style>