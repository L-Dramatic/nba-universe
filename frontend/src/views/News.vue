<template>
    <div class="bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen py-10">
        <div class="max-w-7xl mx-auto px-6">
            <!-- 标题 -->
            <div class="mb-8">
                <h1 class="text-4xl font-black text-gray-900 mb-2">NBA Hot News</h1>
                <p class="text-gray-600">Stay updated with the latest NBA headlines</p>
            </div>

            <!-- 加载状态 -->
            <LoadingSpinner v-if="store.isLoading" />
            
            <!-- 错误状态 -->
            <ErrorMessage v-if="store.error" :message="store.error" />

            <!-- 新闻网格 -->
            <div v-if="!store.isLoading && newsArticles.length > 0" 
                class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div 
                    v-for="(article, index) in newsArticles" 
                    :key="index"
                    class="bg-white rounded-xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden cursor-pointer transform hover:-translate-y-1">
                    
                    <!-- 新闻图片 -->
                    <div class="h-48 overflow-hidden bg-gray-200">
                        <img 
                            v-if="article.urlToImage"
                            :src="article.urlToImage" 
                            :alt="article.title"
                            class="w-full h-full object-cover"
                            @error="handleImageError"
                        />
                        <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-blue-500 to-blue-700">
                            <svg class="w-16 h-16 text-white opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                            </svg>
                        </div>
                    </div>

                    <!-- 新闻内容 -->
                    <div class="p-5">
                        <!-- 来源和时间 -->
                        <div class="flex items-center justify-between mb-3 text-xs text-gray-500">
                            <span class="font-semibold">{{ article.source?.name || 'NBA News' }}</span>
                            <span>{{ formatDate(article.publishedAt) }}</span>
                        </div>

                        <!-- 标题 -->
                        <h3 class="text-lg font-bold text-gray-900 mb-2 line-clamp-2 hover:text-blue-600 transition-colors">
                            {{ article.title }}
                        </h3>

                        <!-- 描述 -->
                        <p class="text-sm text-gray-600 mb-4 line-clamp-3">
                            {{ article.description || 'Click to read more...' }}
                        </p>

                        <!-- Read More 按钮 -->
                        <a 
                            :href="article.url" 
                            target="_blank"
                            rel="noopener noreferrer"
                            class="inline-flex items-center text-blue-600 font-semibold hover:text-blue-700 transition-colors"
                            @click.stop>
                            Read More
                            <svg class="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                            </svg>
                        </a>
                    </div>
                </div>
            </div>

            <!-- 无数据 -->
            <div v-if="!store.isLoading && newsArticles.length === 0 && !store.error" 
                class="text-center py-20 bg-white rounded-xl shadow">
                <div class="text-6xl mb-4">📰</div>
                <h2 class="text-2xl font-bold text-gray-700">No News Available</h2>
                <p class="text-gray-500 mt-2">Check back later for the latest NBA news.</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useNbaStore } from '../stores/nbaStore';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import ErrorMessage from '../components/ui/ErrorMessage.vue';

const store = useNbaStore();
const newsArticles = computed(() => store.hotNews || []);

// 格式化日期
const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
};

// 处理图片加载错误
const handleImageError = (event) => {
    event.target.style.display = 'none';
};

// 组件加载时获取新闻
onMounted(() => {
    store.fetchHotNews();
});
</script>

<style scoped>
/* 限制文本行数 */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>

