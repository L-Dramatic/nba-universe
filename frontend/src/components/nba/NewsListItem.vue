<template>
    <li class="mb-4 last:mb-0">
        <a :href="article.url" target="_blank" rel="noopener noreferrer"
            class="block bg-white rounded-lg shadow-md hover:shadow-xl transition-shadow duration-300 overflow-hidden group">
            <div class="flex flex-col sm:flex-row">
                <!-- 新闻封面图片 -->
                <div class="sm:w-64 h-48 sm:h-auto flex-shrink-0 bg-gray-200 relative overflow-hidden">
                    <img v-if="article.urlToImage" 
                        :src="article.urlToImage" 
                        :alt="article.title"
                        @error="imageError = true"
                        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                        loading="lazy">
                    <!-- 无图片时的占位 -->
                    <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-gray-300 to-gray-400">
                        <svg class="w-16 h-16 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
                        </svg>
                    </div>
                </div>
                
                <!-- 新闻内容 -->
                <div class="flex-1 p-4">
                    <!-- 新闻标题 -->
                    <h3 class="text-lg font-bold text-gray-900 group-hover:text-blue-600 transition-colors line-clamp-2 mb-2">
                        {{ article.title }}
                    </h3>
                    
                    <!-- 新闻描述 -->
                    <p v-if="article.description" class="text-sm text-gray-600 line-clamp-2 mb-3">
                        {{ article.description }}
                    </p>
                    
                    <!-- 新闻元信息 -->
                    <div class="flex items-center justify-between text-xs text-gray-500">
                        <div class="flex items-center space-x-2">
                            <!-- 来源 -->
                            <span class="font-semibold">{{ article.source.name }}</span>
                            <span>•</span>
                            <!-- 发布时间 -->
                            <span>{{ formatDate(article.publishedAt) }}</span>
                        </div>
                        <!-- 阅读指示 -->
                        <span class="text-blue-600 font-semibold group-hover:underline">Read More →</span>
                    </div>
                </div>
            </div>
        </a>
    </li>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
    article: {
        type: Object,
        required: true
    }
});

const imageError = ref(false);

// 格式化日期
const formatDate = (dateString) => {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) {
        return 'Today';
    } else if (diffDays === 1) {
        return 'Yesterday';
    } else if (diffDays < 7) {
        return `${diffDays} days ago`;
    } else {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
    }
};
</script>

<style scoped>
/* 限制文本行数 */
.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
</style>