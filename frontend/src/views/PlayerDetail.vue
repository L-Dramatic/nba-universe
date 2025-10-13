<template>
    <div class="container mx-auto">
        <LoadingSpinner v-if="isLoading" />
        <ErrorMessage v-if="error" :message="error" />

        <div v-if="playerData" class="space-y-8 animate-fade-in">

            <!-- 球员基础信息 (已修复) -->
            <div
                class="bg-white p-8 rounded-2xl shadow-lg flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-8">
                <!-- 头像部分 (已更新为真实照片 + 备用方案) -->
                <div class="w-32 h-32 flex-shrink-0">
                    <img v-if="!imageHasError"
                        :src="`https://cdn.nba.com/headshots/nba/latest/1040x760/${playerData.player_info.id}.png`"
                        @error="onImageError"
                        class="w-full h-full rounded-full object-cover border-4 border-gray-300 bg-gray-200"
                        alt="Player Headshot">
                    <!-- 图片加载失败时的备用头像 -->
                    <div v-else
                        class="w-32 h-32 bg-gray-200 rounded-full flex items-center justify-center border-4 border-gray-300">
                        <span class="text-6xl font-bold text-gray-500">
                            {{ playerData.player_info.firstname?.charAt(0) }}{{
                                playerData.player_info.lastname?.charAt(0) }}
                        </span>
                    </div>
                </div>

                <!-- 名字和队名部分 (已修复) -->
                <div>
                    <h1 class="text-4xl font-bold text-center sm:text-left">{{ playerData.player_info.firstname }} {{
                        playerData.player_info.lastname }}</h1>
                    <router-link v-if="playerData.player_info.team?.id"
                        :to="{ name: 'team-detail', params: { teamName: playerData.player_info.team.name.toLowerCase() } }"
                        class="text-xl text-gray-600 hover:text-blue-600 transition-colors flex items-center justify-center sm:justify-start mt-2">
                        <img :src="playerData.player_info.team.logo" class="h-8 w-8 mr-2" />
                        {{ playerData.player_info.team.name }}
                    </router-link>
                    <p v-else class="text-xl text-gray-600 text-center sm:text-left mt-2">Free Agent</p>
                </div>
            </div>

            <!-- 赛季选择器 (使用硬编码列表) -->
            <div class="flex justify-end items-center">
                <label for="season-select" class="mr-2 font-semibold text-gray-700">Season:</label>
                <select id="season-select" v-model="selectedSeason"
                    class="p-2 border-2 border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500">
                    <option v-for="year in availableSeasons" :key="year" :value="year">
                        {{ year }}-{{ parseInt(year) + 1 }}
                    </option>
                </select>
            </div>

            <!-- 球员赛季平均数据 -->
            <section>
                <SectionTitle>{{ selectedSeason }}-{{ parseInt(selectedSeason) + 1 }} Season Averages</SectionTitle>
                <div v-if="!isLoading && playerData.statistics && playerData.statistics.games_played > 0"
                    class="grid grid-cols-2 md:grid-cols-3 gap-4">
                    <StatBox label="Games Played" :value="playerData.statistics.games_played" />
                    <StatBox label="Points" :value="playerData.statistics.points" />
                    <StatBox label="Rebounds" :value="playerData.statistics.rebounds" />
                    <StatBox label="Assists" :value="playerData.statistics.assists" />
                    <StatBox label="Steals" :value="playerData.statistics.steals" />
                    <StatBox label="Blocks" :value="playerData.statistics.blocks" />
                </div>
                <div v-else class="text-gray-500 p-4">No statistics available for this season.</div>
            </section>

            <!-- 最新新闻 -->
            <section v-if="playerData.news && playerData.news.length > 0">
                <SectionTitle>Latest News</SectionTitle>
                <div class="bg-white rounded-lg shadow-md overflow-hidden">
                    <ul class="divide-y divide-gray-200">
                        <NewsListItem v-for="(article, index) in playerData.news.slice(0, 5)" :key="index"
                            :article="article" />
                    </ul>
                </div>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useNbaStore } from '../stores/nbaStore';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import ErrorMessage from '../components/ui/ErrorMessage.vue';
import SectionTitle from '../components/ui/SectionTitle.vue';
import StatBox from '../components/nba/StatBox.vue';
import NewsListItem from '../components/nba/NewsListItem.vue';

const props = defineProps({
    playerId: { type: [String, Number], required: true }
});

const store = useNbaStore();
const playerData = ref(null);
const isLoading = ref(true);
const error = ref(null);

// 状态：用于处理图片加载失败
const imageHasError = ref(false);

const onImageError = () => {
    imageHasError.value = true;
};

// 回归到硬编码的赛季列表
const selectedSeason = ref('2023');
const availableSeasons = ref(['2023', '2022', '2021', '2020', '2019']);

// 获取数据的函数
const fetchData = async (season) => {
    isLoading.value = true;
    error.value = null;
    imageHasError.value = false; // 每次获取新数据时，重置图片错误状态

    const data = await store.fetchPlayerDetails(props.playerId, season);

    if (data) {
        playerData.value = data;
    } else {
        error.value = store.error || `Failed to load details for player ID ${props.playerId} in season ${season}.`;
    }
    isLoading.value = false;
};

// 监听 selectedSeason 的变化，重新获取数据
watch(selectedSeason, (newSeason, oldSeason) => {
    if (newSeason && newSeason !== oldSeason) {
        fetchData(newSeason);
    }
});

// 组件加载时，获取一次默认赛季的数据
onMounted(() => {
    fetchData(selectedSeason.value);
});
</script>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.5s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}
</style>