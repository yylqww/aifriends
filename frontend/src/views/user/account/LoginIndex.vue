<script setup lang="ts">

</script>


<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100">
    <div class="w-full max-w-md px-6">
      <fieldset class="fieldset bg-white rounded-2xl shadow-xl border-0 p-8">
        <div class="space-y-4">
          <div>
            <label class="label text-sm font-medium text-gray-700 mb-1">用户名</label>
            <input
              type="email"
              class="input w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
              placeholder="用户名"
            />
          </div>

          <div>
            <label class="label text-sm font-medium text-gray-700 mb-1">密码</label>
            <input
              type="password"
              class="input w-full rounded-lg border-gray-300 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 transition-all"
              placeholder="密码"
            />
          </div>

          <div class="flex items-center justify-between text-sm">
            <label class="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" class="checkbox checkbox-sm rounded" />
              <span class="text-gray-600">记住我</span>
            </label>
            <a href="#" class="text-blue-600 hover:text-blue-700 hover:underline">忘记密码？</a>
          </div>

          <button class="btn btn-primary w-full bg-blue-600 hover:bg-blue-700 border-0 rounded-lg py-3 font-semibold transition-all transform hover:scale-[1.02]">
            登录
          </button>

          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
          </div>
        </div>

        <p class="text-center text-sm text-gray-600 mt-6">
          还没有账号？
          <RouterLink :to="{name: 'user-account-register-index'}" class="text-blue-600 hover:text-blue-700 font-semibold hover:underline">立即注册</RouterLink>
        </p>
      </fieldset>
    </div>
  </div>
</template>


<style scoped>

</style>