import httpx
from app.core.config import WEATHER_API_KEY

API_URL = "https://api.openweathermap.org/data/2.5/weather"

async def get_weather_by_city(city: str):
    """
    根据城市名称获取当前天气
    """
    if not WEATHER_API_KEY:
        return None

    async with httpx.AsyncClient() as client:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric" # 使用摄氏度
        }
        
        try:
            response = await client.get(API_URL, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"OpenWeatherMap API error: {e}")
            return None