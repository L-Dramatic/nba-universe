<template>
    <div v-if="weatherData" class="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl p-6 shadow-lg">
        <h3 class="text-xl font-bold text-gray-800 mb-4 flex items-center">
            <svg class="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M3 15a4 4 0 004 4h9a5 5 0 10-.1-9.999 5.002 5.002 0 10-9.78 2.096A4.001 4.001 0 003 15z"></path>
            </svg>
            Weather Information
        </h3>

        <!-- 当前天气 -->
        <div v-if="current" class="mb-6">
            <div class="flex items-center justify-between mb-4">
                <div>
                    <div class="text-5xl font-bold text-gray-800">
                        {{ Math.round(current.main.temp) }}°C
                    </div>
                    <div class="text-lg text-gray-600 capitalize mt-1">
                        {{ current.weather[0].description }}
                    </div>
                    <div class="text-sm text-gray-500 mt-1">
                        Feels like {{ Math.round(current.main.feels_like) }}°C
                    </div>
                </div>
                <div class="text-center">
                    <img 
                        :src="`https://openweathermap.org/img/wn/${current.weather[0].icon}@4x.png`" 
                        :alt="current.weather[0].description"
                        class="w-24 h-24"
                    />
                </div>
            </div>

            <!-- 详细信息网格 -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div class="bg-white/60 rounded-lg p-3">
                    <div class="text-xs text-gray-500 mb-1">Humidity</div>
                    <div class="text-lg font-semibold text-blue-600">{{ current.main.humidity }}%</div>
                </div>
                <div class="bg-white/60 rounded-lg p-3">
                    <div class="text-xs text-gray-500 mb-1">Wind Speed</div>
                    <div class="text-lg font-semibold text-blue-600">{{ current.wind.speed }} m/s</div>
                </div>
                <div class="bg-white/60 rounded-lg p-3">
                    <div class="text-xs text-gray-500 mb-1">Pressure</div>
                    <div class="text-lg font-semibold text-blue-600">{{ current.main.pressure }} hPa</div>
                </div>
                <div class="bg-white/60 rounded-lg p-3">
                    <div class="text-xs text-gray-500 mb-1">Visibility</div>
                    <div class="text-lg font-semibold text-blue-600">{{ (current.visibility / 1000).toFixed(1) }} km</div>
                </div>
            </div>

            <!-- 日出日落 -->
            <div v-if="current.sys" class="mt-3 flex justify-around text-sm">
                <div class="flex items-center text-gray-600">
                    <svg class="w-5 h-5 mr-1 text-yellow-500" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd"></path>
                    </svg>
                    Sunrise: {{ formatTime(current.sys.sunrise) }}
                </div>
                <div class="flex items-center text-gray-600">
                    <svg class="w-5 h-5 mr-1 text-orange-500" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path>
                    </svg>
                    Sunset: {{ formatTime(current.sys.sunset) }}
                </div>
            </div>
        </div>

        <!-- 空气质量 -->
        <div v-if="airQuality" class="mb-6 bg-white/60 rounded-lg p-4">
            <h4 class="font-semibold text-gray-700 mb-2 flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Air Quality Index
            </h4>
            <div class="flex items-center">
                <div 
                    class="text-2xl font-bold mr-3"
                    :class="getAQIColor(airQuality.list[0].main.aqi)"
                >
                    {{ getAQILabel(airQuality.list[0].main.aqi) }}
                </div>
                <div class="text-sm text-gray-600">
                    PM2.5: {{ airQuality.list[0].components.pm2_5.toFixed(1) }} μg/m³
                </div>
            </div>
        </div>

        <!-- 天气预报 -->
        <div v-if="forecast && forecast.list" class="mt-4">
            <h4 class="font-semibold text-gray-700 mb-3 flex items-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                        d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
                </svg>
                24-Hour Forecast
            </h4>
            <div class="grid grid-cols-4 gap-2">
                <div 
                    v-for="(item, index) in forecast.list.slice(0, 4)" 
                    :key="index"
                    class="bg-white/60 rounded-lg p-2 text-center"
                >
                    <div class="text-xs text-gray-500 mb-1">
                        {{ formatForecastTime(item.dt) }}
                    </div>
                    <img 
                        :src="`https://openweathermap.org/img/wn/${item.weather[0].icon}@2x.png`" 
                        :alt="item.weather[0].description"
                        class="w-12 h-12 mx-auto"
                    />
                    <div class="text-sm font-semibold text-gray-800">
                        {{ Math.round(item.main.temp) }}°C
                    </div>
                    <div class="text-xs text-gray-600">
                        {{ item.weather[0].main }}
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    weatherData: {
        type: Object,
        default: null
    }
});

// 提取天气数据的各个部分
const current = computed(() => props.weatherData?.current);
const forecast = computed(() => props.weatherData?.forecast);
const airQuality = computed(() => props.weatherData?.air_quality);

// 格式化时间戳为本地时间
const formatTime = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
};

// 格式化预报时间
const formatForecastTime = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString('en-US', { hour: '2-digit' });
};

// 获取空气质量等级标签
const getAQILabel = (aqi) => {
    const labels = {
        1: 'Good',
        2: 'Fair',
        3: 'Moderate',
        4: 'Poor',
        5: 'Very Poor'
    };
    return labels[aqi] || 'Unknown';
};

// 获取空气质量颜色
const getAQIColor = (aqi) => {
    const colors = {
        1: 'text-green-600',
        2: 'text-yellow-600',
        3: 'text-orange-600',
        4: 'text-red-600',
        5: 'text-purple-600'
    };
    return colors[aqi] || 'text-gray-600';
};
</script>

<style scoped>
/* 添加一些平滑的过渡效果 */
.bg-white\/60 {
    transition: all 0.3s ease;
}

.bg-white\/60:hover {
    background-color: rgba(255, 255, 255, 0.8);
    transform: translateY(-2px);
}
</style>


