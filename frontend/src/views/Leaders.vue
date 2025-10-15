<template>
    <div class="bg-gradient-to-br from-gray-50 to-gray-100 min-h-screen">
        <div class="max-w-6xl mx-auto px-12 py-10">
            <!-- 顶部区域 -->
            <div class="mb-10">
                <!-- 标题和赛季选择 -->
                <div class="text-center mb-8">
                    <h1 class="text-5xl font-black text-gray-900 mb-4 tracking-tight">
                        League Leaders
                    </h1>
                    
                    <!-- 赛季选择器 -->
                    <div class="flex justify-center items-center gap-3 mb-4">
                        <label class="text-gray-600 font-medium">Season:</label>
                        <select 
                            v-model="selectedSeason"
                            @change="onSeasonChange"
                            class="px-4 py-2 bg-white border-2 border-gray-300 rounded-lg text-gray-700 font-semibold focus:outline-none focus:border-blue-500 cursor-pointer">
                            <option value="2023">2023-24</option>
                            <option value="2022">2022-23</option>
                            <option value="2021">2021-22</option>
                        </select>
                    </div>
                </div>
                
                <!-- 类别选择 -->
                <div class="flex justify-center gap-3 flex-wrap">
                    <button 
                        v-for="cat in categories" 
                        :key="cat.value" 
                        @click="selectCategory(cat.value)"
                        :class="[
                            'px-6 py-3 text-base font-semibold rounded-lg border-2 transition-all duration-200',
                            selectedCategory === cat.value
                                ? 'bg-blue-600 text-white border-blue-600 shadow-lg'
                                : 'bg-white text-gray-700 border-gray-300 hover:border-blue-400 hover:text-blue-600'
                        ]">
                        {{ cat.label }}
                    </button>
                </div>
            </div>

            <!-- 加载与错误 -->
            <LoadingSpinner v-if="store.isLoading" />
            <ErrorMessage v-if="store.error" :message="store.error" />

            <!-- 排行榜表格 -->
            <div v-if="!store.isLoading && leaders.length > 0" class="overflow-x-auto bg-white rounded-xl shadow-xl border border-gray-200">
                <table class="w-full">
                    <thead class="bg-gradient-to-r from-gray-100 to-gray-50 border-b-2 border-gray-300">
                        <tr>
                            <th class="px-6 py-4 text-left text-base font-bold text-gray-700 uppercase tracking-wide w-20">#</th>
                            <th class="px-6 py-4 text-left text-base font-bold text-gray-700 uppercase tracking-wide">Player</th>
                            <th class="px-6 py-4 text-center text-base font-bold text-gray-700 uppercase tracking-wide w-28">Team</th>
                            <th class="px-6 py-4 text-center text-base font-bold text-gray-700 uppercase tracking-wide w-24">GP</th>
                            <th class="px-6 py-4 text-center text-base font-bold text-gray-700 uppercase tracking-wide w-28 bg-blue-50">{{ getStatKey() }}</th>
                            <th class="px-6 py-4 text-center text-base font-bold text-gray-700 uppercase tracking-wide w-24 hidden md:table-cell">MIN</th>
                            <th class="px-6 py-4 text-center text-base font-bold text-gray-700 uppercase tracking-wide w-24 hidden lg:table-cell">PTS</th>
                            <th class="px-6 py-4 text-center text-base font-bold text-gray-700 uppercase tracking-wide w-24 hidden lg:table-cell">REB</th>
                            <th class="px-6 py-4 text-center text-base font-bold text-gray-700 uppercase tracking-wide w-24 hidden lg:table-cell">AST</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-200">
                        <tr 
                            v-for="(player, index) in leaders" 
                            :key="player.PLAYER_ID"
                            @click="goToPlayer(player.PLAYER_ID)"
                            :class="[
                                'hover:bg-blue-50 hover:shadow-sm cursor-pointer transition-all duration-150',
                                index === 0 ? 'bg-gradient-to-r from-amber-100 via-yellow-50 to-transparent border-l-4 border-amber-500' :
                                index === 1 ? 'bg-gradient-to-r from-cyan-100 via-blue-50 to-transparent border-l-4 border-cyan-500' :
                                index === 2 ? 'bg-gradient-to-r from-orange-100 via-orange-50 to-transparent border-l-4 border-orange-500' : ''
                            ]">
                            <!-- 排名 -->
                            <td class="px-6 py-5 text-center">
                                <span :class="[
                                    'inline-flex items-center justify-center w-10 h-10 rounded-full text-lg font-black bg-white border-2',
                                    index === 0 ? 'border-yellow-500 text-yellow-600 shadow-md' :
                                    index === 1 ? 'border-cyan-500 text-cyan-600 shadow-md' :
                                    index === 2 ? 'border-orange-500 text-orange-600 shadow-md' :
                                    'border-gray-300 text-gray-700 shadow-sm'
                                ]">
                                    {{ index + 1 }}
                                </span>
                            </td>
                            
                            <!-- 球员 -->
                            <td class="px-6 py-5">
                                <div class="flex items-center gap-4">
                                    <img 
                                        v-if="player.nba_official_id"
                                        :src="getPlayerAvatarUrl(player.nba_official_id)" 
                                        :alt="player.PLAYER"
                                        class="w-12 h-12 rounded-full object-cover border-2 border-gray-200 shadow-md"
                                        @error="handleImageError"
                                    />
                                    <div v-else class="w-12 h-12 rounded-full bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center text-white text-base font-bold flex-shrink-0 shadow-md">
                                        {{ getInitials(player.PLAYER) }}
                                    </div>
                                    <span class="text-lg font-semibold text-gray-900">{{ player.PLAYER }}</span>
                                </div>
                            </td>
                            
                            <!-- 球队 -->
                            <td class="px-6 py-5 text-center">
                                <span class="inline-block px-3 py-1 bg-gray-100 rounded-md text-base font-semibold text-gray-800">{{ getTeamAbbr(player) }}</span>
                            </td>
                            
                            <!-- 比赛场数 -->
                            <td class="px-6 py-5 text-center text-lg font-medium text-gray-700">
                                {{ player.GP }}
                            </td>
                            
                            <!-- 主要统计 -->
                            <td class="px-6 py-5 text-center bg-blue-50">
                                <span class="text-xl font-bold text-blue-600">
                                    {{ formatStat(player[getStatKey()]) }}
                                </span>
                            </td>
                            
                            <!-- 上场时间 -->
                            <td class="px-6 py-5 text-center text-lg font-medium text-gray-700 hidden md:table-cell">
                                {{ formatStat(player.MIN) }}
                            </td>
                            
                            <!-- PTS -->
                            <td class="px-6 py-5 text-center text-lg font-medium text-gray-700 hidden lg:table-cell">
                                {{ formatStat(player.PTS) }}
                            </td>
                            
                            <!-- REB -->
                            <td class="px-6 py-5 text-center text-lg font-medium text-gray-700 hidden lg:table-cell">
                                {{ formatStat(player.REB) }}
                            </td>
                            
                            <!-- AST -->
                            <td class="px-6 py-5 text-center text-lg font-medium text-gray-700 hidden lg:table-cell">
                                {{ formatStat(player.AST) }}
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <!-- 无数据 -->
            <div v-if="!store.isLoading && leaders.length === 0 && !store.error" 
                class="text-center py-12 text-gray-500">
                No data available
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useNbaStore } from '../stores/nbaStore';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import ErrorMessage from '../components/ui/ErrorMessage.vue';

const store = useNbaStore();
const router = useRouter();
const selectedCategory = ref('points');
const selectedSeason = ref('2023');

const categories = [
    { value: 'points', label: 'Points', statKey: 'PTS' },
    { value: 'rebounds', label: 'Rebounds', statKey: 'REB' },
    { value: 'assists', label: 'Assists', statKey: 'AST' },
    { value: 'steals', label: 'Steals', statKey: 'STL' },
    { value: 'blocks', label: 'Blocks', statKey: 'BLK' }
];

const leaders = computed(() => {
    const key = `${selectedCategory.value}_${selectedSeason.value}`;
    return store.leaders[key] || [];
});

const selectCategory = async (category) => {
    selectedCategory.value = category;
    await fetchLeadersData();
};

const onSeasonChange = async () => {
    await fetchLeadersData();
};

const fetchLeadersData = async () => {
    const key = `${selectedCategory.value}_${selectedSeason.value}`;
    // 如果缓存中没有数据，则请求
    if (!store.leaders[key]) {
        await store.fetchLeaders(selectedCategory.value, selectedSeason.value);
    }
};

const getPlayerAvatarUrl = (nbaOfficialId) => {
    return `https://cdn.nba.com/headshots/nba/latest/1040x760/${nbaOfficialId}.png`;
};

const getInitials = (playerName) => {
    if (!playerName) return '?';
    const names = playerName.split(' ');
    return names.length >= 2 ? names[0][0] + names[names.length - 1][0] : playerName[0];
};

const handleImageError = (event) => {
    event.target.style.display = 'none';
};

const getTeamAbbr = (player) => {
    return player.TEAM_ABBREVIATION || player.TEAM || '-';
};

const getStatKey = () => {
    const category = categories.find(cat => cat.value === selectedCategory.value);
    return category ? category.statKey : 'PTS';
};

const formatStat = (value) => {
    if (value === null || value === undefined) return '0.0';
    return typeof value === 'number' ? value.toFixed(1) : value;
};

const goToPlayer = (playerId) => {
    if (playerId) {
        router.push({ name: 'player-detail', params: { playerId } });
    }
};

onMounted(() => {
    fetchLeadersData();
});
</script>

<style scoped>
/* 表格样式 */
table {
    border-collapse: collapse;
}

/* 行高 */
tbody tr {
    height: 72px;
}

/* 平滑过渡 */
tbody tr:hover {
    transform: translateX(2px);
}

/* 确保下划线显示在按钮下方 */
button {
    position: relative;
}
</style>
