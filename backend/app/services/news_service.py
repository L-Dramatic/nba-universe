import httpx
from app.core.config import NEWS_API_KEY

API_URL = "https://newsapi.org/v2/everything"

async def get_news_by_keyword(keyword: str, page_size: int = 10):
    """
    根据关键词搜索新闻文章
    """
    # 确保我们有API Key，否则直接返回空
    if not NEWS_API_KEY:
        return {"articles": []}

    async with httpx.AsyncClient() as client:
        # 准备请求参数
        params = {
            "q": keyword,
            "pageSize": page_size,
            "apiKey": NEWS_API_KEY,
            "language": "en" # 可以限定语言为英语
        }
        
        try:
            response = await client.get(API_URL, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            # 如果API返回错误（比如额度用完），打印错误并返回空列表
            print(f"NewsAPI error: {e}")
            return {"articles": []}