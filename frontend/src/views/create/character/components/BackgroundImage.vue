<script setup lang="ts">
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/components/navbar/icons/CameraIcon.vue";
import Croppie from "croppie";
import "croppie/croppie.css";

const props = defineProps<{
  backgroundImage?: string
}>()
const myBackgroundImage = ref(props.backgroundImage || '')

watch(() => props.backgroundImage, newVal =>{
  myBackgroundImage.value = newVal || ''
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef =  useTemplateRef('croppie-ref')
let croppie: Croppie | null = null;

async function openModal(photo: string) {
  modalRef.value?.showModal();
  await nextTick()

  if(!croppie){
    croppie = new Croppie(croppieRef.value!, {
      // 保持长方形比例，符合手机聊天背景感
      viewport: {width: 240, height: 400, type: 'square'},
      boundary: {width: 450, height: 500},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }
  croppie.bind({ url: photo })
}

async function crop(){
  if(!croppie) return
  myBackgroundImage.value = await croppie.result({
    type: 'base64',
    size: { width: 720, height: 1200 },
    format: 'jpeg',
    quality: 0.9
  })
  await modalRef.value?.close()
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

defineExpose({ myBackgroundImage })
</script>

<template>
  <div class="form-control w-full group">
    <label class="label text-sm font-medium text-gray-700 mb-1.5 transition-all duration-300 group-focus-within:text-blue-600 group-focus-within:translate-x-0.5">
      聊天背景
    </label>

    <div class="flex items-start gap-6">
      <div class="relative w-24 h-40 rounded-xl overflow-hidden shadow-md border-2 border-gray-100 bg-gray-50 transition-transform duration-300 hover:scale-[1.02]">
        <img v-if="myBackgroundImage" :src="myBackgroundImage" class="w-full h-full object-cover" />
        <div v-else class="w-full h-full flex items-center justify-center bg-gray-100">
           <CameraIcon class="text-gray-300 w-8 h-8" />
        </div>

        <div @click="fileInputRef?.click()"
             class="absolute inset-0 bg-black/40 opacity-0 hover:opacity-100 transition-opacity duration-300 flex flex-col justify-center items-center cursor-pointer">
          <CameraIcon class="text-white w-6 h-6 mb-1" />
          <span class="text-[10px] text-white font-bold uppercase tracking-tighter">更换背景</span>
        </div>
      </div>

      <div class="flex-1 pt-2">
        <h4 class="text-xs font-semibold text-gray-600 mb-1">背景预览</h4>
        <p class="text-[11px] text-gray-400 leading-relaxed">
          建议上传比例为 9:16 的图片，<br>
          这会让聊天界面看起来更自然。
        </p>
      </div>
    </div>
  </div>

  <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box bg-white p-6 rounded-2xl border-0 shadow-2xl max-w-lg">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-bold text-gray-800">裁剪聊天背景</h3>
        <button @click="modalRef?.close()" class="btn btn-sm btn-circle btn-ghost">✕</button>
      </div>

      <div ref="croppie-ref" class="overflow-hidden rounded-xl bg-gray-50" />

      <div class="modal-action flex justify-between gap-3 mt-6">
        <button @click="modalRef?.close()" class="btn btn-ghost px-6 rounded-lg text-gray-400 text-xs">
          取消
        </button>
        <button @click="crop" class="btn bg-blue-600 hover:bg-blue-700 border-0 text-white px-8 rounded-lg text-xs font-bold shadow-lg shadow-blue-200">
          确认裁剪
        </button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

:deep(.cr-boundary) {
  border-radius: 12px;
}
:deep(.cr-viewport) {
  border: 2px solid #fff;
  border-radius: 8px;
  box-shadow: 0 0 0 1000px rgba(0,0,0,0.5);
}
</style>