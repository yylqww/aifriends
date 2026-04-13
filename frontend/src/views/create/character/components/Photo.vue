<script setup lang="ts">
import { nextTick, onBeforeUnmount, ref, useTemplateRef, watch } from "vue";
import CameraIcon from "@/components/navbar/icons/CameraIcon.vue";
import Croppie from "croppie";
import "croppie/croppie.css"; // 确保引入样式

const props = defineProps<{
  photo?: string
}>()
const myPhoto = ref(props.photo || '')

watch(() => props.photo, newVal => {
  myPhoto.value = newVal || ''
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef = useTemplateRef('croppie-ref')
let croppie: Croppie | null = null;

async function openModal(photo: string) {
  modalRef.value?.showModal();
  await nextTick()

  if (!croppie) {
    croppie = new Croppie(croppieRef.value!, {
      viewport: { width: 200, height: 200, type: 'square' },
      boundary: { width: 300, height: 300 },
      enableOrientation: true,
      enforceBoundary: true,
    })
  }
  croppie.bind({ url: photo })
}

async function crop() {
  if (!croppie) return
  myPhoto.value = await croppie.result({
    type: 'base64',
    size: { width: 600, height: 600 },
    format: 'png',
    quality: 1
  })
  modalRef.value?.close()
}

function onFileChange(e: Event) {
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];
  target.value = '';
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    if (typeof reader.result === 'string') {
      openModal(reader.result);
    }
  };
  reader.readAsDataURL(file);
}

onBeforeUnmount(() => {
  croppie?.destroy()
})

defineExpose({ myPhoto })
</script>

<template>
  <div class="flex flex-col items-center group">
    <div class="avatar relative reveal-card">
      <div class="w-28 h-28 rounded-full ring-4 ring-white shadow-lg overflow-hidden border border-gray-100 bg-gray-50 transition-transform duration-500 group-hover:scale-105">
        <img v-if="myPhoto" :src="myPhoto" class="w-full h-full object-cover" />
        <div v-else class="w-full h-full flex items-center justify-center bg-gray-100">
           <CameraIcon class="text-gray-300 w-10 h-10" />
        </div>

        <div @click="fileInputRef?.click()"
             class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-all duration-300 flex flex-col justify-center items-center cursor-pointer">
          <CameraIcon class="text-white w-8 h-8 mb-1 scale-90 group-hover:scale-100 transition-transform" />
          <span class="text-[10px] text-white/90 font-bold uppercase tracking-tighter">更换头像</span>
        </div>
      </div>
    </div>
  </div>

  <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">

  <dialog ref="modal-ref" class="modal modal-bottom sm:modal-middle">
    <div class="modal-box bg-white p-6 rounded-2xl border-0 shadow-2xl transition-all">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-bold text-gray-800">裁剪角色头像</h3>
        <button @click="modalRef?.close()" class="btn btn-sm btn-circle btn-ghost">✕</button>
      </div>

      <div ref="croppie-ref" class="flex flex-col justify-center overflow-hidden rounded-xl bg-gray-50" />

      <div class="modal-action flex justify-between gap-3 pt-2">
        <button @click="modalRef?.close()" class="btn btn-ghost px-6 rounded-lg text-gray-500 text-xs">
          取消
        </button>
        <button @click="crop" class="btn bg-blue-600 hover:bg-blue-700 border-0 text-white px-8 rounded-lg text-xs font-bold shadow-lg shadow-blue-200">
          保存修改
        </button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

:deep(.cr-boundary) {
  border-radius: 12px;
  background-color: #f9fafb;
}
:deep(.cr-viewport) {
  border: 2px solid #fff;
  box-shadow: 0 0 0 1000px rgba(0, 0, 0, 0.4);
  border-radius: 8px;
}
:deep(.cr-slider) {
  width: 180px;
  margin-top: 20px;
}
</style>