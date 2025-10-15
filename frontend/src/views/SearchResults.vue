<template>
    <div class="container mx-auto p-8">
        <h1 class="text-3xl font-bold mb-6">Search Results for: <span class="text-blue-600">"{{ query }}"</span></h1>

        <LoadingSpinner v-if="store.isLoading" />
        <ErrorMessage v-if="store.error" :message="store.error" />

        <div v-if="!store.isLoading && store.teams.length === 0 && store.players.length === 0"
            class="text-center py-16">
            <h2 class="text-2xl text-gray-700">No results found.</h2>
            <p class="text-gray-500 mt-2">Please try a different search term.</p>
        </div>

        <div v-if="!store.isLoading" class="grid grid-cols-1 lg:grid-cols-2 gap-12">
      <!-- 球队结果 -->
<div v-if="store.teams.length > 0">
  <SectionTitle>Teams</SectionTitle>
  <div class="space-y-4">
    <!-- 将 v-for 循环里的内容替换成这个 -->
    <router-link v-for="team in store.teams" :key="team.id" :to="{ name: 'team-detail', params: { teamName: team.name.toLowerCase() } }" class="flex items-center p-4 bg-white rounded-xl shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
      <img :src="team.logo" class="w-12 h-12 mr-5"/>
      <div>
        <!-- 只显示队名，因为 city 等信息在这个接口里也不一定有 -->
        <span class="font-bold text-lg text-gray-800">{{ team.name }}</span>
        <!-- <p class="text-sm text-gray-500">{{ team.leagues.standard.conference }} Conference</p>  <-- 删除或注释掉这一行 -->
      </div>
    </router-link>
  </div>
</div>

            <!-- 球员结果 -->
            <div v-if="store.players.length > 0">
                <SectionTitle>Players</SectionTitle>
                <div class="space-y-4">
                    <router-link v-for="player in store.players" :key="player.id"
                        :to="{ name: 'player-detail', params: { playerId: player.id } }"
                        class="flex items-center p-4 bg-white rounded-xl shadow-md hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                        <!-- 球员头像（真实照片或首字母备用） -->
                        <div class="w-12 h-12 mr-5 flex-shrink-0">
                            <img v-if="player.nba_official_id"
                                :src="`https://cdn.nba.com/headshots/nba/latest/1040x760/${player.nba_official_id}.png`"
                                @error="e => e.target.style.display='none'"
                                class="w-full h-full rounded-full object-cover border-2 border-gray-200"
                                :alt="`${player.firstname} ${player.lastname}`">
                            <!-- 备用首字母头像 -->
                            <div v-if="!player.nba_official_id"
                                class="w-full h-full bg-gradient-to-br from-blue-600 to-blue-800 rounded-full flex items-center justify-center font-bold text-white text-xl">
                                {{ player.firstname.charAt(0) }}{{ player.lastname.charAt(0) }}
                            </div>
                        </div>
                        <div>
                            <p class="font-bold text-lg text-gray-800">{{ player.firstname }} {{ player.lastname }}</p>
                        </div>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useNbaStore } from '../stores/nbaStore';
import { onMounted } from 'vue';
import LoadingSpinner from '../components/ui/LoadingSpinner.vue';
import ErrorMessage from '../components/ui/ErrorMessage.vue';
import SectionTitle from '../components/ui/SectionTitle.vue';

const props = defineProps({
    query: { type: String, required: true }
});

const store = useNbaStore();

onMounted(() => {
    store.searchAll(props.query);
});
</script>