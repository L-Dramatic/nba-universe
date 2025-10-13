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
                class="bg-white rounded-xl shadow-lg p-6 flex items-center justify-between">

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
                </div>

                <!-- 客队信息 -->
                <div class="flex items-center justify-end w-2/5">
                    <span class="text-xl font-bold text-gray-800 text-right">{{ game.teams.visitors.name }}</span>
                    <img :src="game.teams.visitors.logo" class="h-12 w-12 ml-4" />
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

// 格式化时间 (例如: 19:00)
const formatTime = (isoString) => {
    const date = new Date(isoString);
    // 转换为本地时间显示
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', hour12: false });
};

// 监听 selectedDate 的变化，一旦变化就重新获取数据
watch(selectedDate, fetchGames);

// 组件加载时，获取一次当天的数据
onMounted(fetchGames);
</script>