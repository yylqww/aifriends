<script setup lang="ts">
import {nextTick, onBeforeMount, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/components/navbar/icons/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])
const myPhoto = ref(props.photo)

watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref')
const modalRef = useTemplateRef('modal-ref')
const croppieRef =  useTemplateRef('croppie-ref')
let croppie: Croppie | null = null;



// 2. 修改函数定义，接收一个 string 类型的参数
async function openModal(photo: string) {
  // 将传进来的图片存起来

  // 打开模态框
  modalRef.value?.showModal();
  await nextTick()

  if(!croppie){
    croppie = new Croppie(croppieRef.value!, {
      viewport: {width: 200, height: 200, type: 'square'},
      boundary: {width: 300, height: 300},
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
  myPhoto.value = await croppie.result({
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
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div class="w-28 rounded-full">
        <img :src="myPhoto" />
        <div @click="fileInputRef?.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
          <CameraIcon />
        </div>
      </div>
    </div>
  </div>
  <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
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
