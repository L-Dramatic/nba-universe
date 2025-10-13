import httpx
from app.core.config import UNSPLASH_API_KEY

API_URL = "https://api.unsplash.com/search/photos"

async def get_image_url_by_keyword(keyword: str):
    """
    根据关键词从Unsplash获取一张高质量图片的URL
    """
    if not UNSPLASH_API_KEY:
        return None

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Client-ID {UNSPLASH_API_KEY}"}
        params = {
            "query": f"{keyword} city", # 优化搜索词，增加"city"提高相关性
            "per_page": 1,
            "orientation": "landscape" # 获取横向图片，更适合做背景
        }
        
        try:
            response = await client.get(API_URL, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            
            # 从返回结果中提取图片的URL
            if data and data.get("results"):
                # 我们选择 regular 尺寸的图片，大小适中
                return data["results"][0]["urls"]["regular"]
            return None
        except httpx.HTTPStatusError as e:
            print(f"Unsplash API error: {e}")
            return None