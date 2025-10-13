<template>
    <header class="bg-gray-800 text-white p-4 shadow-md">
        <nav class="container mx-auto flex justify-between items-center">
            <router-link to="/" class="text-2xl font-bold hover:text-gray-300">
                🏀 NBA Universe
            </router-link>
            <div class="space-x-4">
                <router-link to="/" class="hover:text-gray-300">Home</router-link>
                <!-- 我们先把其他页面的链接占位，以后再启用 -->
                <span class="text-gray-500">Schedule</span>
                <span class="text-gray-500">Leaders</span>
            </div>
        </nav>
    </header>
</template>

<script setup>
// 这个组件很简单，不需要复杂的逻辑
</script>

<style scoped>
/* 使用Tailwind，我们几乎不需要写scoped CSS */
</style>