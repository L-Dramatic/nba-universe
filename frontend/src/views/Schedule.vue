<template>
    <div class="container mx-auto">
        <SectionTitle>NBA Game Schedule</SectionTitle>

        <!-- 1. 日期选择器 -->
        <div class="mb-8 flex items-center justify-center space-x-4">
            <button @click="changeDate(-1)" class="p-2 rounded-full bg-gray-200 hover:bg-gray-300 transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
            </button>
            <input type="date" v-model="selectedDate"
                class="p-2 text-lg font-semibold border-2 border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500">
            <button @click="changeDate(1)" class="p-2 rounded-full bg-gray-200 hover:bg-gray-300 transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
            </button>
        </div>

        <!-- 2. 加载与错误状态 -->
        <LoadingSpinner v-if="store.isLoading" />
        <ErrorMessage v-if="store.error" :message="store.error" />

        <!-- 3. 比赛列表 -->
        <div v-if="!store.isLoading && games.length > 0" class="space-y-6">
            <div v-for="game in games" :key="game.id"
                @click="openGameDetail(game)"
                class="bg-white rounded-xl shadow-lg p-6 flex items-center justify-between cursor-pointer hover:shadow-2xl hover:scale-[1.02] transition-all duration-300">

                <!-- 主队信息 -->
                <div class="flex items-center w-2/5">
                    <img :src="game.teams.home.logo" class="h-12 w-12 mr-4" />
                    <span class="text-xl font-bold text-gray-800">{{ game.teams.home.name }}</span>
                </div>

                <!-- 比分/时间信息 -->
                <div class="text-center">
                    <div v-if="game.scores.home.points !== null" class="text-3xl font-bold">
                        <span>{{ game.scores.home.points }}</span>
                        <span class="mx-2">-</span>
                        <span>{{ game.scores.visitors.points }}</span>
                    </div>
                    <div v-else class="text-lg font-semibold text-gray-500">
                        {{ formatTime(game.date.start) }}
                    </div>
                    <div class="text-xs text-gray-400 mt-1">
                        {{ game.status.long }}
                    </div>
                    <!-- 点击提示 -->
                    <div class="text-xs text-blue-600 mt-2 font-semibold">
                        Click for details →
                    </div>
                </div>

                <!-- 客队信息 -->
                <div class="flex items-center justify-end w-2/5">
                    <span class="text-xl font-bold text-gray-800 text-right">{{ game.teams.visitors.name }}</span>
                    <img :src="game.teams.visitors.logo" class="h-12 w-12 ml-4" />
                </div>

            </div>
        </div>

        <!-- 比赛详情模态框 -->
        <div v-if="selectedGame" @click="closeGameDetail" 
            class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4 animate-fade-in">
            <div @click.stop class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto animate-slide-up">
                <!-- 模态框头部 -->
                <div class="sticky top-0 bg-gradient-to-r from-blue-600 to-purple-600 text-white p-6 rounded-t-2xl">
                    <div class="flex justify-between items-center">
                        <h2 class="text-2xl font-bold">Game Details</h2>
                        <button @click="closeGameDetail" class="text-white hover:text-gray-200 transition">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- 模态框内容 -->
                <div class="p-6 space-y-6">
                    <!-- 比赛对阵 -->
                    <div class="flex items-center justify-between">
                        <!-- 主队 -->
                        <router-link :to="{ name: 'team-detail', params: { teamName: selectedGame.teams.home.name.toLowerCase() } }"
                            class="flex flex-col items-center space-y-2 hover:bg-gray-50 p-4 rounded-lg transition group">
                            <img :src="selectedGame.teams.home.logo" class="h-20 w-20" />
                            <span class="text-lg font-bold text-gray-800 group-hover:text-blue-600">{{ selectedGame.teams.home.name }}</span>
                            <span class="text-sm text-gray-500">Home</span>
                        </router-link>

                        <!-- 比分 -->
                        <div class="text-center px-8">
                            <div v-if="selectedGame.scores.home.points !== null" class="space-y-2">
                                <div class="text-5xl font-bold text-gray-900">
                                    {{ selectedGame.scores.home.points }} - {{ selectedGame.scores.visitors.points }}
                                </div>
                                <div class="text-sm font-semibold text-gray-600 uppercase tracking-wide">
                                    {{ selectedGame.status.long }}
                                </div>
                            </div>
                            <div v-else class="space-y-2">
                                <div class="text-2xl font-bold text-gray-600">
                                    VS
                                </div>
                                <div class="text-lg font-semibold text-gray-500">
                                    {{ formatFullTime(selectedGame.date.start) }}
                                </div>
                            </div>
                        </div>

                        <!-- 客队 -->
                        <router-link :to="{ name: 'team-detail', params: { teamName: selectedGame.teams.visitors.name.toLowerCase() } }"
                            class="flex flex-col items-center space-y-2 hover:bg-gray-50 p-4 rounded-lg transition group">
                            <img :src="selectedGame.teams.visitors.logo" class="h-20 w-20" />
                            <span class="text-lg font-bold text-gray-800 group-hover:text-blue-600">{{ selectedGame.teams.visitors.name }}</span>
                            <span class="text-sm text-gray-500">Away</span>
                        </router-link>
                    </div>

                    <!-- 比赛信息 -->
                    <div class="bg-gray-50 rounded-xl p-6 space-y-4">
                        <h3 class="text-lg font-bold text-gray-900 mb-4">Game Information</h3>
                        
                        <div class="grid grid-cols-2 gap-4">
                            <!-- 日期 -->
                            <div class="flex items-start space-x-3">
                                <svg class="w-5 h-5 text-blue-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm text-gray-500">Date</p>
                                    <p class="font-semibold text-gray-900">{{ formatFullDate(selectedGame.date.start) }}</p>
                                </div>
                            </div>

                            <!-- 时间 -->
                            <div class="flex items-start space-x-3">
                                <svg class="w-5 h-5 text-green-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm text-gray-500">Time</p>
                                    <p class="font-semibold text-gray-900">{{ formatFullTime(selectedGame.date.start) }}</p>
                                </div>
                            </div>

                            <!-- 场馆 -->
                            <div class="flex items-start space-x-3" v-if="selectedGame.arena?.name">
                                <svg class="w-5 h-5 text-purple-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path>
                                </svg>
                                <div>
                                    <p class="text-sm text-gray-500">Arena</p>
                                    <p class="font-semibold text-gray-900">{{ selectedGame.arena.name }}</p>
                                    <p class="text-xs text-gray-600" v-if="selectedGame.arena.city">{{ selectedGame.arena.city }}, {{ selectedGame.arena.state }}</p>
                                </div>
                            </div>

                            <!-- 状态 -->
                            <div class="flex items-start space-x-3">
                                <svg class="w-5 h-5 text-orange-600 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                                <div>
                                    <p class="text-sm text-gray-500">Status</p>
                                    <p class="font-semibold text-gray-900">{{ selectedGame.status.long }}</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- 分节比分（如果有） -->
                    <div v-if="selectedGame.scores.home.points !== null && selectedGame.periods" class="bg-gray-50 rounded-xl p-6">
                        <h3 class="text-lg font-bold text-gray-900 mb-4">Quarter Scores</h3>
                        <div class="overflow-x-auto">
                            <table class="w-full text-center">
                                <thead>
                                    <tr class="border-b-2 border-gray-300">
                                        <th class="pb-2 text-left">Team</th>
                                        <th class="pb-2" v-for="(period, index) in selectedGame.periods.total" :key="index">Q{{ index + 1 }}</th>
                                        <th class="pb-2 font-bold">Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr class="border-b border-gray-200">
                                        <td class="py-3 text-left font-semibold">{{ selectedGame.teams.home.name }}</td>
                                        <td class="py-3" v-for="(score, index) in selectedGame.scores.home.linescore" :key="index">{{ score }}</td>
                                        <td class="py-3 font-bold text-lg">{{ selectedGame.scores.home.points }}</td>
                                    </tr>
                                    <tr>
                                        <td class="py-3 text-left font-semibold">{{ selectedGame.teams.visitors.name }}</td>
                                        <td class="py-3" v-for="(score, index) in selectedGame.scores.visitors.linescore" :key="index">{{ score }}</td>
                                        <td class="py-3 font-bold text-lg">{{ selectedGame.scores.visitors.points }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- 无比赛提示 -->
        <div v-if="!store.isLoading && games.length === 0" class="text-center py-16">
            <h2 class="text-2xl text-gray-700">No Games Scheduled</h2>
            <p class="text-gray-500 mt-2">There are no games on this date.</p>
        </div>

    </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue';
import { useNbaStore } from '../stores/nbaStore';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import ErrorMessage from '../components/ui/ErrorMessage.vue';
import SectionTitle from '../components/ui/SectionTitle.vue';

const store = useNbaStore();
const selectedDate = ref(new Date().toISOString().split('T')[0]); // 默认为今天
const games = computed(() => store.schedule); // 从store中获取比赛数据
const selectedGame = ref(null); // 选中的比赛详情

// 获取赛程的函数
const fetchGames = () => {
    store.fetchSchedule(selectedDate.value);
};

// 切换日期 (向前/向后一天)
const changeDate = (days) => {
    const currentDate = new Date(selectedDate.value);
    currentDate.setDate(currentDate.getDate() + days);
    selectedDate.value = currentDate.toISOString().split('T')[0];
};

// 打开比赛详情
const openGameDetail = (game) => {
    selectedGame.value = game;
    // 阻止body滚动
    document.body.style.overflow = 'hidden';
};

// 关闭比赛详情
const closeGameDetail = () => {
    selectedGame.value = null;
    // 恢复body滚动
    document.body.style.overflow = '';
};

// 格式化时间 (例如: 19:00)
const formatTime = (isoString) => {
    const date = new Date(isoString);
    // 转换为本地时间显示
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
};

// 格式化完整时间 (例如: 7:00 PM)
const formatFullTime = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit', hour12: true });
};

// 格式化完整日期 (例如: Monday, October 16, 2025)
const formatFullDate = (isoString) => {
    const date = new Date(isoString);
    return date.toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
};

// 监听 selectedDate 的变化，一旦变化就重新获取数据
watch(selectedDate, fetchGames);

// 组件加载时，获取一次当天的数据
onMounted(fetchGames);
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.3s ease-out;
}

.animate-slide-up {
    animation: slideUp 0.3s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }
    to {
        opacity: 1;
    }
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>