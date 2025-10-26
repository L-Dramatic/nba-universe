import httpx
import asyncio
from app.core.config import WEATHER_API_KEY

# OpenWeatherMap API 不同端点
CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"
AIR_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"

async def get_weather_by_city(city: str):
    """
    根据城市名称获取当前天气
    """
    if not WEATHER_API_KEY:
        print("Warning: WEATHER_API_KEY not configured")
        return None
    
    if not city or city.strip() == "":
        print("Warning: Empty city name provided")
        return None

    async with httpx.AsyncClient() as client:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric" # 使用摄氏度
        }
        
        try:
            response = await client.get(CURRENT_WEATHER_URL, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"✓ Weather data fetched successfully for {city}")
            return data
        except httpx.HTTPStatusError as e:
            print(f"✗ OpenWeatherMap API error for city '{city}': {e.response.status_code} - {e.response.text if hasattr(e.response, 'text') else 'No details'}")
            return None
        except Exception as e:
            print(f"✗ Unexpected error fetching weather for '{city}': {e}")
            return None

async def get_weather_forecast(city: str):
    """
    获取5天天气预报（每3小时一个数据点）
    调用 OpenWeatherMap 的 5 Day / 3 Hour Forecast API
    """
    if not WEATHER_API_KEY or not city:
        return None
    
    async with httpx.AsyncClient() as client:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric",
            "cnt": 8  # 获取未来24小时的预报（8个3小时间隔）
        }
        
        try:
            response = await client.get(FORECAST_URL, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"✓ Weather forecast fetched for {city}")
            return data
        except Exception as e:
            print(f"✗ Failed to fetch forecast for {city}: {e}")
            return None

async def get_air_quality(lat: float, lon: float):
    """
    获取空气质量数据
    调用 OpenWeatherMap 的 Air Pollution API
    需要经纬度坐标
    """
    if not WEATHER_API_KEY or not lat or not lon:
        return None
    
    async with httpx.AsyncClient() as client:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": WEATHER_API_KEY
        }
        
        try:
            response = await client.get(AIR_POLLUTION_URL, params=params)
            response.raise_for_status()
            data = response.json()
            print(f"✓ Air quality data fetched for coordinates ({lat}, {lon})")
            return data
        except Exception as e:
            print(f"✗ Failed to fetch air quality: {e}")
            return None

async def get_comprehensive_weather(city: str):
    """
    综合获取天气信息：
    1. 当前天气 (Current Weather API)
    2. 天气预报 (5 Day Forecast API)
    3. 空气质量 (Air Pollution API)
    
    这样调用了OpenWeatherMap的3个不同API端点，体现API集成的丰富性
    """
    if not city:
        return None
    
    # 首先获取当前天气（包含经纬度信息）
    current_weather = await get_weather_by_city(city)
    
    if not current_weather:
        return None
    
    # 提取经纬度用于空气质量查询
    lat = current_weather.get("coord", {}).get("lat")
    lon = current_weather.get("coord", {}).get("lon")
    
    # 并发获取预报和空气质量数据
    forecast_task = get_weather_forecast(city)
    air_quality_task = get_air_quality(lat, lon) if lat and lon else None
    
    if air_quality_task:
        forecast, air_quality = await asyncio.gather(
            forecast_task,
            air_quality_task,
            return_exceptions=True
        )
    else:
        forecast = await forecast_task
        air_quality = None
    
    # 组合所有数据
    return {
        "current": current_weather,
        "forecast": forecast if forecast and not isinstance(forecast, Exception) else None,
        "air_quality": air_quality if air_quality and not isinstance(air_quality, Exception) else None
    }