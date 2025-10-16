<template>
    <div>
        <LoadingSpinner v-if="isLoading" />
        <ErrorMessage v-if="error" :message="error" />

        <div v-if="teamData" class="space-y-12 animate-fade-in">

            <!-- 1. 顶部头图 (增强版) -->
            <header
                class="h-72 md:h-96 rounded-2xl bg-cover bg-center relative text-white flex items-center justify-center shadow-2xl overflow-hidden"
                :style="{ backgroundImage: `url(${teamData.city_context.image_url})` }">
                <!-- 渐变遮罩层，更有电影感 -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
                <div class="relative text-center p-4">
                    <img :src="teamData.team_info.logo"
                        class="h-28 w-28 md:h-36 md:w-36 mx-auto mb-4 transition-transform duration-500 hover:scale-110" />
                    <h1 class="text-4xl md:text-6xl font-black tracking-tighter text-shadow">
                        {{ teamData.team_info.name }}
                    </h1>
                </div>
            </header>

            <!-- 2. 城市背景 & 关键数据 (增强版) -->
            <section>
                <SectionTitle>City Context & Key Info</SectionTitle>
                <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
                    <StatBox label="City" :value="teamData.team_info.city" />
                    <StatBox v-if="teamData.city_context.weather" label="Weather"
                        :value="`${Math.round(teamData.city_context.weather.main.temp)}°C`"
                        :subtext="teamData.city_context.weather.weather[0].description" />
                    <StatBox label="Conference" :value="teamData.team_info.leagues.standard.conference" />
                    <StatBox label="Division" :value="teamData.team_info.leagues.standard.division" />
                </div>
            </section>

            <!-- 3. 球员名单 (增强版) -->
            <section>
                <div class="flex justify-between items-center mb-6">
                    <SectionTitle>Team Roster</SectionTitle>
                    <!-- 赛季选择器 -->
                    <div class="flex items-center space-x-3">
                        <label for="season-select" class="font-semibold text-gray-700">Season:</label>
                        <select id="season-select" v-model="selectedSeason"
                            class="p-2 border-2 border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 bg-white">
                            <option v-for="year in availableSeasons" :key="year" :value="year">
                                {{ year }}-{{ parseInt(year) + 1 }}
                            </option>
                        </select>
                    </div>
                </div>
                <div v-if="isLoadingRoster" class="text-center py-12">
                    <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
                    <p class="mt-4 text-gray-600">Loading roster...</p>
                </div>
                <div v-else-if="teamData.roster && teamData.roster.length > 0" class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
                    <!-- 我们在PlayerCard上添加了过渡效果 -->
                    <transition-group name="list">
                        <PlayerCard v-for="(player, index) in teamData.roster" :key="player.id" :player="player"
                            :style="{ transitionDelay: `${index * 50}ms` }" />
                    </transition-group>
                </div>
                <div v-else class="bg-gray-50 rounded-lg p-8 text-center">
                    <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
                    </svg>
                    <p class="text-lg text-gray-600 font-semibold">No Roster Data Available</p>
                    <p class="text-sm text-gray-500 mt-2">No players found for the {{ selectedSeason }}-{{ parseInt(selectedSeason) + 1 }} season</p>
                </div>
            </section>

            <!-- 4. 最新新闻 (卡片式布局) -->
            <section>
                <SectionTitle>Latest News</SectionTitle>
                
                <!-- 有新闻时显示 -->
                <div v-if="teamData.news && teamData.news.length > 0">
                    <ul class="space-y-4">
                        <NewsListItem v-for="(article, index) in displayedNews" :key="index"
                            :article="article" />
                    </ul>
                    
                    <!-- Load More 按钮 -->
                    <div v-if="hasMoreNews" class="mt-6 text-center">
                        <button 
                            @click="loadMoreNews"
                            class="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg">
                            Load More News
                        </button>
                    </div>
                    
                    <!-- 没有更多新闻的提示 -->
                    <div v-else-if="newsToShow > 5" class="mt-6 text-center text-gray-500 italic">
                        No more news available
                    </div>
                </div>
                
                <!-- 没有新闻时显示 -->
                <div v-else class="bg-gray-50 rounded-lg p-8 text-center">
                    <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"></path>
                    </svg>
                    <p class="text-lg text-gray-600 font-semibold">No Related News Available</p>
                    <p class="text-sm text-gray-500 mt-2">There are currently no news articles about this team</p>
                </div>
            </section>

        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useNbaStore } from '../stores/nbaStore';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import ErrorMessage from '../components/ui/ErrorMessage.vue';
import SectionTitle from '../components/ui/SectionTitle.vue';
import StatBox from '../components/nba/StatBox.vue';
import PlayerCard from '../components/nba/PlayerCard.vue';
import NewsListItem from '../components/nba/NewsListItem.vue';

const props = defineProps({
    teamName: { type: String, required: true }
});
const store = useNbaStore();
const teamData = ref(null);
const isLoading = ref(true);
const error = ref(null);

// 赛季选择器
const availableSeasons = ['2023', '2022', '2021']; // 免费 API 支持的赛季
const selectedSeason = ref('2023');
const isLoadingRoster = ref(false);

// 新闻分页
const newsToShow = ref(5);

// 计算属性：显示的新闻列表
const displayedNews = computed(() => {
    if (!teamData.value?.news) return [];
    return teamData.value.news.slice(0, newsToShow.value);
});

// 计算属性：是否还有更多新闻
const hasMoreNews = computed(() => {
    if (!teamData.value?.news) return false;
    return newsToShow.value < teamData.value.news.length;
});

// 加载更多新闻
const loadMoreNews = () => {
    newsToShow.value += 5;
};

// 获取球队详情（带赛季参数）
const fetchTeamData = async (season) => {
    try {
        isLoadingRoster.value = true;
        const data = await store.fetchTeamDetails(props.teamName, season);
        if (data) {
            teamData.value = data;
        } else {
            error.value = store.error || 'Failed to load team data.';
        }
    } catch (err) {
        console.error('Error fetching team data:', err);
        error.value = 'Failed to load team data.';
    } finally {
        isLoadingRoster.value = false;
    }
};

// 监听赛季变化
watch(selectedSeason, async (newSeason) => {
    if (teamData.value) {
        await fetchTeamData(newSeason);
    }
});

onMounted(async () => {
    isLoading.value = true;
    await fetchTeamData(selectedSeason.value);
    isLoading.value = false;
});
</script>

<style scoped>
/* 定义Vue的过渡动画 */
.animate-fade-in {
    animation: fadeIn 0.8s ease-out forwards;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.text-shadow {
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

/* 列表项的交错动画 */
.list-enter-active,
.list-leave-active {
    transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
    opacity: 0;
    transform: translateY(30px);
}
</style>