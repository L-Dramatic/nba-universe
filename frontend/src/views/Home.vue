<template>
    <!-- h-[calc(100vh-theme(space.20))] 计算屏幕高度减去顶部栏高度 -->
    <div
        class="relative h-[calc(100vh-5.5rem)] flex items-center justify-center text-center p-4 overflow-hidden -m-4 sm:-m-6 lg:-m-8">
        <!-- 图片轮播背景 -->
        <div v-for="(image, index) in bgImages" :key="image"
            class="absolute inset-0 w-full h-full bg-cover bg-center transition-opacity duration-2000 ease-in-out"
            :class="index === currentImageIndex ? 'opacity-100' : 'opacity-0'"
            :style="{ backgroundImage: `url(${image})` }">
        </div>
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 to-black/20"></div>

        <!-- 内容层 -->
        <div class="relative z-20 animate-fade-in-up">
            <h1 class="text-5xl md:text-7xl font-black text-white uppercase tracking-widest text-shadow-lg">
                NBA Universe
            </h1>
            <p class="mt-4 text-lg md:text-xl text-gray-300">
                Where Every Stat Tells a Story.
            </p>

            <!-- 搜索表单 -->
            <form @submit.prevent="executeSearch" class="mt-10 w-full max-w-2xl mx-auto">
                <div class="relative">
                    <input type="text" v-model="searchQuery"
                        class="w-full p-4 pl-6 pr-20 bg-white/20 text-white placeholder-gray-300 rounded-full border border-white/30 backdrop-blur-md shadow-lg text-lg focus:ring-4 focus:ring-white/50 focus:outline-none transition-all duration-300"
                        placeholder="Find Team or Player..." />
                    <button type="submit" :disabled="searchQuery.length < 3"
                        class="absolute inset-y-0 right-0 flex items-center justify-center w-16 h-16 bg-blue-600 text-white rounded-full m-1 hover:bg-blue-700 transition-colors transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-white disabled:bg-gray-400 disabled:cursor-not-allowed">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                            stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';

const searchQuery = ref('');
const router = useRouter(); // 获取路由实例

// 搜索并跳转的函数
const executeSearch = () => {
    if (searchQuery.value.length < 3) return;
    // 使用router.push进行页面跳转
    router.push({ name: 'search-results', params: { query: searchQuery.value } });
};

// --- 图片轮播逻辑 (保持不变) ---
const bgImages = ref([
    '/bg1.png',
    '/bg2.png',
    '/bg3.png',
    '/bg4.png',
]);
const currentImageIndex = ref(0);
let intervalId = null;

onMounted(() => {
    intervalId = setInterval(() => {
        currentImageIndex.value = (currentImageIndex.value + 1) % bgImages.value.length;
    }, 7000);
});

onUnmounted(() => {
    clearInterval(intervalId);
});
</script>

<style scoped>
/* 和上一版一样，主要是动画 */
.text-shadow-lg {
    text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);
}

.animate-fade-in-up {
    animation: fadeInUp 1s ease-out forwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>