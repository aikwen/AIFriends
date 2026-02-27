<script setup>

import Photo from "@/views/create/character/components/Photo.vue";
import Name from "@/views/create/character/components/Name.vue";
import Profile from "@/views/create/character/components/Profile.vue";
import BackgroundImage from "@/views/create/character/components/BackgroundImage.vue";
import {ref, useTemplateRef} from "vue";
import {base64ToFile} from "@/js/utils/base64_to_file.js";
import api from "@/js/http/api.js";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";

const user = useUserStore()
const router = useRouter()

const photoRef = useTemplateRef('photo-ref')
const nameRef = useTemplateRef('name-ref')
const profileRef = useTemplateRef('profile-ref')
const backgroundImageRef = useTemplateRef('background-image-ref')
const errormessage = ref('')

async function handleCreate(){
  const photo = photoRef.value.myPhoto
  const name = nameRef.value.myName?.trim()
  const profile = profileRef.value.myProfile?.trim()
  const backgroundImage = backgroundImageRef.value.myBackgroundImage

  errormessage.value = ''

  if (!photo) {
    errormessage.value = '头像不能为空'
  }else if (!name) {
    errormessage.value = '名字不能为空'
  }else if (!profile) {
    errormessage.value = '角色介绍不能为空'
  }else if (!backgroundImage){
    errormessage.value = '背景不能为空'
  }else{
    const formData = new FormData()

    formData.append('name', name)
    formData.append('profile', profile)
    formData.append('photo', base64ToFile(photo, 'photo.png'))
    formData.append('background_image', base64ToFile(backgroundImage, 'background_image.png'))

    try {
      const res = await api.post('/api/create/character/create/', formData)
      const data = res.data

      if (data.result === 'success') {
        await router.push({
          name: 'user-space-index',
          params: {
            user_id:user.id
          }
        })
      }else{
        errormessage.value = data.result
      }
    }catch(err) {
      console.log(err)
    }
  }

}

</script>

<template>
<div class="flex justify-center">
  <div class="card w-120 bg-base-200 shadow-sm mt-16">
    <div class="card-body">
      <h3 class="text-lg font-bold my-4">创建角色</h3>
      <Photo ref="photo-ref"/>
      <Name ref="name-ref"/>
      <Profile ref="profile-ref"/>
      <BackgroundImage ref="background-image-ref"/>
      <p v-if="errormessage" class="text-sm text-red-500"> {{ errormessage }} </p>
      <div class="flex justify-center">
        <button @click='handleCreate' class="btn btn-neutral w-60 mt-2">创建</button>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>

</style>