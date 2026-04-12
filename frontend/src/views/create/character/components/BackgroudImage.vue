<script setup lang="ts">
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/components/navbar/icons/CameraIcon.vue";
import Croppie from "croppie";

const props = defineProps(['backgroundImage'])
const myBackgroundImage = ref(props.backgroundImage)

watch(() => props.backgroundImage, newVal =>{
  myBackgroundImage.value =newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef =  useTemplateRef('croppie-ref')
let croppie: Croppie | null = null;



async function openModal(photo: string) {

  // 打开模态框
  modalRef.value?.showModal();
  await nextTick()

  if(!croppie){
    croppie = new Croppie(croppieRef.value!, {
      viewport: {width: 300, height: 500},
      boundary: {width: 600, height: 600},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }
  croppie.bind({
    url: photo,
  })
}

async function crop(){
  if(!croppie) return
  myBackgroundImage.value = await croppie.result({
    type: 'base64',
    size:'viewport',
  })
  await modalRef.value?.close()
}

function onFileChange(e: Event) {
  //使用类型断言告诉 TS，e.target 是一个 HTMLInputElement
  const target = e.target as HTMLInputElement;
  const file = target.files?.[0];

  target.value = '';
  if (!file) return;

  const reader = new FileReader();
  reader.onload = () => {
    // 假设 openModal 已定义，这里也要确保传入的是 string
    if (typeof reader.result === 'string') {
      openModal(reader.result);
    }
  };
  reader.readAsDataURL(file);
}

onBeforeUnmount(() => {
  croppie?.destroy()
})

defineExpose({
  myBackgroundImage,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base text-gray-900 mb-1">
      聊天背景
    </label>
    <div class="avatar relative">
      <div v-if="myBackgroundImage" class="w-15 h-25 rounded-box">
        <img :src="myBackgroundImage" alt="">
      </div>
      <div @click="fileInputRef?.click()" v-else class="w-15 h-25 rounded-box bg-base-300">
        <div class="flex justify-center items-center bg-black/20 w-15 h-25 rounded-box left-0 top-0 cursor-pointer">
          <CameraIcon />
        </div>
      </div>
    </div>
  </fieldset>
  <input ref="file-input-ref" type="file" class="hidden" accept="image/*" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none max-w-2xl">
      <button @click="modalRef?.close()" class="btn btn-circle btn-sm btn-ghost absolute right-2 top-2">
        ×
      </button>
      <div ref="croppie-ref" class="flex flex-col justify-center my-4" />

      <div class="modal-action flex justify-between w-full">
        <button @click="modalRef?.close()" class="btn btn-neutral">
          取消
        </button>
        <button @click="crop" class="btn btn-primary">
          确定
        </button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>