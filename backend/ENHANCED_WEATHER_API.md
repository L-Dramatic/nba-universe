# 🌤️ 增强版天气API集成说明

## 📋 概述

本项目现在集成了 **OpenWeatherMap 的 3 个不同 API 端点**，提供丰富的天气和环境信息，充分体现了 Mashup 应用的 API 集成能力。

---

## 🔌 集成的 API 端点

### 1. **Current Weather Data API** ☀️
**端点**: `https://api.openweathermap.org/data/2.5/weather`

**功能**: 获取指定城市的当前天气数据

**返回数据**:
- 🌡️ **温度**: 当前温度、体感温度
- 🌦️ **天气状况**: 描述、图标
- 💧 **湿度**: 空气湿度百分比
- 🌬️ **风速**: 风速（米/秒）
- 📏 **气压**: 大气压力（hPa）
- 👁️ **能见度**: 可见距离（米）
- 🌅 **日出日落**: 本地日出和日落时间
- 📍 **坐标**: 经纬度（用于其他API调用）

**示例代码**:
```python
async def get_weather_by_city(city: str):
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric"
    }
    response = await client.get(CURRENT_WEATHER_URL, params=params)
    return response.json()
```

---

### 2. **5 Day / 3 Hour Forecast API** 📅
**端点**: `https://api.openweathermap.org/data/2.5/forecast`

**功能**: 获取未来5天的天气预报（每3小时一个数据点）

**返回数据**:
- 📊 **预报数据**: 每3小时的温度、天气、湿度、风速等
- ⏰ **时间戳**: 每个预报点的精确时间
- 🌦️ **天气变化**: 观察天气趋势

**配置**: 当前设置为获取未来24小时（8个数据点）

**示例代码**:
```python
async def get_weather_forecast(city: str):
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "cnt": 8  # 未来24小时
    }
    response = await client.get(FORECAST_URL, params=params)
    return response.json()
```

---

### 3. **Air Pollution API** 🌍
**端点**: `https://api.openweathermap.org/data/2.5/air_pollution`

**功能**: 获取指定坐标的空气质量数据

**返回数据**:
- 🏷️ **AQI等级**: 空气质量指数（1-5级）
  - 1 = Good（优）
  - 2 = Fair（良）
  - 3 = Moderate（中等）
  - 4 = Poor（差）
  - 5 = Very Poor（很差）
- 🔬 **污染物浓度**:
  - PM2.5: 细颗粒物
  - PM10: 可吸入颗粒物
  - CO: 一氧化碳
  - NO2: 二氧化氮
  - SO2: 二氧化硫
  - O3: 臭氧

**示例代码**:
```python
async def get_air_quality(lat: float, lon: float):
    params = {
        "lat": lat,
        "lon": lon,
        "appid": WEATHER_API_KEY
    }
    response = await client.get(AIR_POLLUTION_URL, params=params)
    return response.json()
```

---

## 🎯 综合天气函数

为了优化性能和代码组织，创建了 `get_comprehensive_weather()` 函数，它：

1. ✅ **串行获取当前天气** - 先获取经纬度
2. ✅ **并发获取预报和空气质量** - 使用 `asyncio.gather()`
3. ✅ **优雅的错误处理** - 即使某个API失败也不影响其他数据
4. ✅ **统一返回格式** - 将所有数据组合成一个对象

```python
async def get_comprehensive_weather(city: str):
    # 1. 获取当前天气（包含坐标）
    current_weather = await get_weather_by_city(city)
    
    # 2. 提取坐标
    lat = current_weather.get("coord", {}).get("lat")
    lon = current_weather.get("coord", {}).get("lon")
    
    # 3. 并发获取预报和空气质量
    forecast, air_quality = await asyncio.gather(
        get_weather_forecast(city),
        get_air_quality(lat, lon),
        return_exceptions=True
    )
    
    # 4. 返回组合数据
    return {
        "current": current_weather,
        "forecast": forecast,
        "air_quality": air_quality
    }
```

---

## 🎨 前端展示

### WeatherCard 组件功能

新创建的 `WeatherCard.vue` 组件展示了所有天气数据：

#### 1. **当前天气显示**
```vue
<template>
  <!-- 大号温度显示 -->
  <div class="text-5xl">{{ Math.round(current.main.temp) }}°C</div>
  
  <!-- 天气图标 -->
  <img :src="`https://openweathermap.org/img/wn/${icon}@4x.png`" />
  
  <!-- 详细信息网格 -->
  <div class="grid grid-cols-4">
    <div>湿度: {{ humidity }}%</div>
    <div>风速: {{ wind }} m/s</div>
    <div>气压: {{ pressure }} hPa</div>
    <div>能见度: {{ visibility }} km</div>
  </div>
</template>
```

#### 2. **日出日落时间**
```javascript
const formatTime = (timestamp) => {
    const date = new Date(timestamp * 1000);
    return date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
};
```

#### 3. **空气质量指数**
- 动态颜色显示（绿色=优，红色=差）
- PM2.5浓度显示
- 中英文等级标签

#### 4. **24小时预报**
- 4个时间段的天气卡片
- 温度趋势
- 天气图标和描述

---

## 📊 数据流程图

```
前端访问 /team/:teamName
    ↓
后端 get_team_details()
    ↓
调用 get_comprehensive_weather(city)
    ↓
┌─────────────────────────────────────┐
│  1. Current Weather API             │
│     → 温度、湿度、风速、坐标         │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  2. Forecast API (并发)             │
│     → 未来24小时预报                 │
│                                     │
│  3. Air Pollution API (并发)        │
│     → 空气质量指数、PM2.5            │
└─────────────────────────────────────┘
    ↓
组合数据返回前端
    ↓
WeatherCard 组件渲染
```

---

## 🚀 API 使用示例

### 后端调用示例

```python
# 在 main.py 中
weather_data = await weather_service.get_comprehensive_weather("Los Angeles,US")

# 返回的数据结构
{
    "current": {
        "main": {"temp": 22.5, "humidity": 65, "pressure": 1013},
        "weather": [{"description": "clear sky", "icon": "01d"}],
        "wind": {"speed": 3.5},
        "visibility": 10000,
        "sys": {"sunrise": 1234567890, "sunset": 1234598890},
        "coord": {"lat": 34.05, "lon": -118.24}
    },
    "forecast": {
        "list": [
            {"dt": 1234567890, "main": {"temp": 23.1}, "weather": [...]},
            // ... 更多预报点
        ]
    },
    "air_quality": {
        "list": [{
            "main": {"aqi": 2},  // 1-5等级
            "components": {
                "pm2_5": 12.5,
                "pm10": 18.3,
                // ... 其他污染物
            }
        }]
    }
}
```

### 前端使用示例

```vue
<template>
  <WeatherCard :weatherData="teamData.city_context.weather" />
</template>

<script setup>
import WeatherCard from '@/components/nba/WeatherCard.vue';

// weatherData 会自动包含 current, forecast, air_quality
</script>
```

---

## 💡 为什么这样设计？

### 1. **满足作业要求** 📚
- ✅ 调用了3个不同的API端点（同一provider的不同服务）
- ✅ 展示了数据融合能力
- ✅ 体现了Mashup应用的特点

### 2. **技术亮点** 🌟
- ✅ **异步并发**: 使用 `asyncio.gather()` 提高性能
- ✅ **错误容错**: `return_exceptions=True` 确保单个API失败不影响整体
- ✅ **数据融合**: 将多个API的数据智能组合
- ✅ **用户体验**: 丰富的可视化展示

### 3. **实用价值** 🎯
- 球迷可以了解比赛日的天气情况
- 空气质量信息对户外活动有参考价值
- 预报帮助规划观赛行程

---

## 🔧 配置要求

### API Key 获取

1. 访问 https://openweathermap.org/api
2. 注册免费账户
3. 获取 API Key
4. 在 `backend/.env` 中配置：
   ```
   WEATHER_API_KEY=your_api_key_here
   ```

### 免费版限制

**OpenWeatherMap 免费计划**:
- ✅ 60 次请求/分钟
- ✅ 1,000,000 次请求/月
- ✅ 所有3个API端点都可用
- ✅ 不需要信用卡

**注意**: 
- 每次访问球队详情页会调用3个API（如果全部成功）
- 建议添加缓存机制以优化API使用

---

## 📈 未来优化建议

1. **缓存机制** 💾
   ```python
   from cachetools import TTLCache
   weather_cache = TTLCache(maxsize=100, ttl=1800)  # 30分钟
   ```

2. **历史天气数据** 📊
   - 集成 Historical Weather Data API
   - 分析球队主场历史天气模式

3. **天气预警** ⚠️
   - 集成 Weather Alerts API
   - 显示极端天气警告

4. **更多可视化** 📉
   - 温度趋势图表
   - 空气质量历史曲线
   - 降水概率雷达

---

## 📞 调试和测试

### 测试单个API端点

```bash
# 测试当前天气
curl "https://api.openweathermap.org/data/2.5/weather?q=Los%20Angeles,US&appid=YOUR_KEY&units=metric"

# 测试预报
curl "https://api.openweathermap.org/data/2.5/forecast?q=Los%20Angeles,US&appid=YOUR_KEY&units=metric&cnt=8"

# 测试空气质量
curl "https://api.openweathermap.org/data/2.5/air_pollution?lat=34.05&lon=-118.24&appid=YOUR_KEY"
```

### 后端日志

访问球队详情页时，后端会输出：
```
✓ Weather data fetched successfully for Los Angeles,US
✓ Weather forecast fetched for Los Angeles,US
✓ Air quality data fetched for coordinates (34.05, -118.24)
```

---

## 🎓 课程作业价值

这个增强版天气集成展示了：

1. **多API集成能力** - 3个不同端点的协调使用
2. **异步编程技术** - 并发请求优化性能
3. **数据融合思维** - 将不同来源的数据整合成有价值的信息
4. **用户体验设计** - 直观的可视化展示
5. **错误处理机制** - 优雅的降级策略

完全符合《微服务架构》课程对 Mashup 应用的要求！✨

---

## 📚 参考资源

- [OpenWeatherMap API 文档](https://openweathermap.org/api)
- [Current Weather Data](https://openweathermap.org/current)
- [5 Day Forecast](https://openweathermap.org/forecast5)
- [Air Pollution API](https://openweathermap.org/api/air-pollution)


