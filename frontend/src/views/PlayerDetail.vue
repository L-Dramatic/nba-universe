<template>
    <div class="container mx-auto">
        <LoadingSpinner v-if="isLoading" />
        <ErrorMessage v-if="error" :message="error" />

        <div v-if="playerData" class="space-y-8 animate-fade-in">

            <!-- 球员基础信息 (已修复) -->
            <div
                class="bg-white p-8 rounded-2xl shadow-lg flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-8">
                <!-- 头像部分 (NBA 官方照片或首字母备用) -->
                <div class="w-32 h-32 flex-shrink-0 relative">
                    <!-- 如果有 NBA 官方 ID，显示真实照片 -->
                    <img v-if="playerData.player_info.nba_official_id && !imageHasError"
                        :src="`https://cdn.nba.com/headshots/nba/latest/1040x760/${playerData.player_info.nba_official_id}.png`"
                        @error="imageHasError = true"
                        class="w-full h-full rounded-full object-cover border-4 border-white shadow-2xl bg-gray-100"
                        :alt="`${playerData.player_info.firstname} ${playerData.player_info.lastname}`">
                    <!-- 没有 ID 或加载失败时显示首字母头像 -->
                    <div v-else class="w-full h-full rounded-full bg-gradient-to-br from-blue-600 to-blue-800 flex items-center justify-center border-4 border-white shadow-2xl">
                        <span class="text-4xl font-bold text-white tracking-wider">
                            {{ playerData.player_info.firstname?.charAt(0) || '' }}{{ playerData.player_info.lastname?.charAt(0) || '' }}
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
                    <p v-else class="text-xl text-gray-500 italic text-center sm:text-left mt-2">No Team Data</p>
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
                <div v-else class="bg-gray-50 rounded-lg p-8 text-center">
                    <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
                    </svg>
                    <p class="text-lg text-gray-600 font-semibold">No Statistics Available</p>
                    <p class="text-sm text-gray-500 mt-2">
                        Unable to find statistics for {{ playerData.player_info.firstname }} {{ playerData.player_info.lastname }} 
                        in the {{ selectedSeason }}-{{ parseInt(selectedSeason) + 1 }} season.
                    </p>
                    <p class="text-xs text-gray-400 mt-2">This player may not have played any games during this season or the data is unavailable.</p>
                </div>
            </section>

            <!-- 球员基础信息 -->
            <section v-if="playerData.player_info">
                <SectionTitle>Player Information</SectionTitle>
                <div class="bg-white rounded-2xl shadow-lg p-6">
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <!-- 身高 -->
                        <div class="flex items-start space-x-3" v-if="playerData.player_info.height">
                            <div class="flex-shrink-0 w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">Height</p>
                                <p class="text-lg font-bold text-gray-900">
                                    {{ playerData.player_info.height.feets }}'{{ playerData.player_info.height.inches }}" 
                                    <span class="text-sm text-gray-600">({{ playerData.player_info.height.meters }}m)</span>
                                </p>
                            </div>
                        </div>

                        <!-- 体重 -->
                        <div class="flex items-start space-x-3" v-if="playerData.player_info.weight">
                            <div class="flex-shrink-0 w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 6l3 1m0 0l-3 9a5.002 5.002 0 006.001 0M6 7l3 9M6 7l6-2m6 2l3-1m-3 1l-3 9a5.002 5.002 0 006.001 0M18 7l3 9m-3-9l-6-2m0-2v2m0 16V5m0 16H9m3 0h3"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">Weight</p>
                                <p class="text-lg font-bold text-gray-900">
                                    {{ playerData.player_info.weight.pounds }} lbs 
                                    <span class="text-sm text-gray-600">({{ playerData.player_info.weight.kilograms }}kg)</span>
                                </p>
                            </div>
                        </div>

                        <!-- 生日和年龄 -->
                        <div class="flex items-start space-x-3" v-if="playerData.player_info.birth">
                            <div class="flex-shrink-0 w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">Birthday</p>
                                <p class="text-lg font-bold text-gray-900">{{ formatDate(playerData.player_info.birth.date) }}</p>
                                <p class="text-sm text-gray-600">{{ calculateAge(playerData.player_info.birth.date) }} years old</p>
                            </div>
                        </div>

                        <!-- 国籍 -->
                        <div class="flex items-start space-x-3" v-if="playerData.player_info.birth?.country">
                            <div class="flex-shrink-0 w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3.055 11H5a2 2 0 012 2v1a2 2 0 002 2 2 2 0 012 2v2.945M8 3.935V5.5A2.5 2.5 0 0010.5 8h.5a2 2 0 012 2 2 2 0 104 0 2 2 0 012-2h1.064M15 20.488V18a2 2 0 012-2h3.064M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">Country</p>
                                <p class="text-lg font-bold text-gray-900">{{ playerData.player_info.birth.country }}</p>
                            </div>
                        </div>

                        <!-- 位置 -->
                        <div class="flex items-start space-x-3" v-if="playerData.player_info.leagues?.standard?.pos">
                            <div class="flex-shrink-0 w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">Position</p>
                                <p class="text-lg font-bold text-gray-900">{{ getPositionFullName(playerData.player_info.leagues.standard.pos) }}</p>
                                <p class="text-sm text-gray-600">{{ playerData.player_info.leagues.standard.pos }}</p>
                            </div>
                        </div>

                        <!-- 球衣号码 -->
                        <div class="flex items-start space-x-3" v-if="playerData.player_info.leagues?.standard?.jersey">
                            <div class="flex-shrink-0 w-10 h-10 bg-indigo-100 rounded-lg flex items-center justify-center">
                                <span class="text-lg font-bold text-indigo-600">#</span>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">Jersey Number</p>
                                <p class="text-lg font-bold text-gray-900">#{{ playerData.player_info.leagues.standard.jersey }}</p>
                            </div>
                        </div>

                        <!-- NBA 开始年份 -->
                        <div class="flex items-start space-x-3" v-if="playerData.player_info.nba?.start">
                            <div class="flex-shrink-0 w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">NBA Debut</p>
                                <p class="text-lg font-bold text-gray-900">{{ playerData.player_info.nba.start }}</p>
                                <p class="text-sm text-gray-600" v-if="playerData.player_info.nba.pro">{{ playerData.player_info.nba.pro }} years pro</p>
                            </div>
                        </div>

                        <!-- 大学/高中 -->
                        <div class="flex items-start space-x-3 md:col-span-2" v-if="playerData.player_info.college">
                            <div class="flex-shrink-0 w-10 h-10 bg-teal-100 rounded-lg flex items-center justify-center">
                                <svg class="w-6 h-6 text-teal-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path d="M12 14l9-5-9-5-9 5 9 5z"></path>
                                    <path d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5zm0 0l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14zm-4 6v-7.5l4-2.222"></path>
                                </svg>
                            </div>
                            <div>
                                <p class="text-sm text-gray-500 font-medium">College / High School</p>
                                <p class="text-lg font-bold text-gray-900">{{ playerData.player_info.college }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- 最新新闻 -->
            <section>
                <SectionTitle>Latest News</SectionTitle>
                
                <!-- 有新闻时显示 -->
                <div v-if="playerData.news && playerData.news.length > 0">
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
                    <p class="text-sm text-gray-500 mt-2">There are currently no news articles about this player</p>
                </div>
            </section>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
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

// 图片加载状态
const imageHasError = ref(false);

// 新闻分页
const newsToShow = ref(5);

// 计算属性：显示的新闻列表
const displayedNews = computed(() => {
    if (!playerData.value?.news) return [];
    return playerData.value.news.slice(0, newsToShow.value);
});

// 计算属性：是否还有更多新闻
const hasMoreNews = computed(() => {
    if (!playerData.value?.news) return false;
    return newsToShow.value < playerData.value.news.length;
});

// 加载更多新闻
const loadMoreNews = () => {
    newsToShow.value += 5;
};

// 格式化日期
const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
};

// 计算年龄
const calculateAge = (dateString) => {
    if (!dateString) return 'N/A';
    const birthDate = new Date(dateString);
    const today = new Date();
    let age = today.getFullYear() - birthDate.getFullYear();
    const monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
};

// 获取位置全称
const getPositionFullName = (pos) => {
    const positions = {
        'G': 'Guard',
        'F': 'Forward',
        'C': 'Center',
        'G-F': 'Guard-Forward',
        'F-G': 'Forward-Guard',
        'F-C': 'Forward-Center',
        'C-F': 'Center-Forward'
    };
    return positions[pos] || pos;
};

// 赛季列表（免费 API 计划只支持 2021-2023 赛季）
const selectedSeason = ref('2023');
const availableSeasons = ref(['2023', '2022', '2021']);

// 获取数据的函数
const fetchData = async (season) => {
    isLoading.value = true;
    error.value = null;
    imageHasError.value = false; // 重置图片错误状态
    newsToShow.value = 5; // 重置新闻显示数量

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