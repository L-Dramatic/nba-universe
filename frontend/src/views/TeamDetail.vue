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
                <SectionTitle>Team Roster (2023-2024)</SectionTitle>
                <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-5">
                    <!-- 我们在PlayerCard上添加了过渡效果 -->
                    <transition-group name="list">
                        <PlayerCard v-for="(player, index) in teamData.roster" :key="player.id" :player="player"
                            :style="{ transitionDelay: `${index * 50}ms` }" />
                    </transition-group>
                </div>
            </section>

            <!-- 4. 最新新闻 (增强版) -->
            <section>
                <SectionTitle>Latest News</SectionTitle>
                <div class="bg-white rounded-lg shadow-md overflow-hidden">
                    <ul class="divide-y divide-gray-200">
                        <NewsListItem v-for="(article, index) in teamData.news.slice(0, 5)" :key="index"
                            :article="article" />
                    </ul>
                </div>
            </section>

        </div>
    </div>
</template>

<script setup>
// Script部分和之前一样，无需改动
import { ref, onMounted } from 'vue';
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

onMounted(async () => {
    const data = await store.fetchTeamDetails(props.teamName);
    if (data) {
        teamData.value = data;
    } else {
        error.value = store.error || 'Failed to load team data.';
    }
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