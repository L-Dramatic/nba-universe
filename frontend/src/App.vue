<template>
  <div class="min-h-screen bg-gray-100 font-sans">

    <!-- 1. 顶部导航栏 (Top Navigation Bar) - 改为蓝色 -->
    <header class="bg-blue-800 shadow-lg sticky top-0 z-50">
      <nav class="container mx-auto flex justify-between items-center p-4">
        <!-- 左侧: Logo 和 项目名 -->
        <router-link to="/" class="flex items-center space-x-3">
          <img src="/nba.png" alt="NBA Logo" class="h-10 w-auto">
          <span class="text-2xl font-bold text-white">NBA Universe</span>
        </router-link>

        <!-- 右侧: 导航链接 -->
        <div class="space-x-6">
          <router-link to="/" class="nav-link text-white">Search</router-link>
          <router-link to="/schedule" class="nav-link text-blue-300">Schedule</router-link>
          <router-link to="/leaders" class="nav-link text-blue-300">Leaders</router-link>
        </div>
      </nav>
    </header>

    <!-- 2. 主内容区 -->
    <main>
      <!-- 注意：我们移除了这里的padding，因为首页和结果页将自己控制布局 -->
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView, RouterLink } from 'vue-router';
</script>

<style>
/* ... style 部分保持不变，但我们可以微调一下激活链接的样式 ... */
.nav-link {
  @apply text-lg font-semibold hover:text-white transition-colors relative;
}

.nav-link::after {
  @apply content-[''] absolute bottom-[-4px] left-0 w-full h-0.5 bg-white transform scale-x-0 origin-left transition-transform duration-300;
}

.router-link-exact-active::after,
.nav-link:hover::after {
  @apply scale-x-100;
}

.router-link-exact-active {
  @apply text-white;
}
</style>