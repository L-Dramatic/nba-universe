import httpx
from app.core.config import NBA_API_KEY

API_URL = "https://v2.nba.api-sports.io"
HEADERS = {
    "x-apisports-key": NBA_API_KEY
}

async def search_team_by_name(name: str):
    """
    根据球队名称搜索球队信息
    """
    # 使用 httpx 异步发送 GET 请求
    async with httpx.AsyncClient() as client:
        # 准备请求参数
        params = {"search": name}
        
        # 发送请求
        response = await client.get(f"{API_URL}/teams", headers=HEADERS, params=params)
        
        # 检查响应状态码，如果不是2xx，则会抛出异常
        response.raise_for_status()
        
        # 返回JSON格式的响应数据
        return response.json()
    
async def search_player_by_name(name: str):
    """
    根据球员名称模糊搜索球员列表
    """
    async with httpx.AsyncClient() as client:
        params = {"search": name}
        response = await client.get(f"{API_URL}/players", headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    
async def get_player_statistics(player_id: int, season: str):
    """
    获取单个球员的统计数据。
    - 如果提供了赛季年份 (e.g., "2023")，则获取该赛季的数据。
    - 如果 season 参数为 "all" 或 None，则不传递 season 参数给API，
      从而获取该球员所有赛季的比赛数据。
    """
    async with httpx.AsyncClient() as client:
        # 基础参数
        params = {"id": player_id}
        
        # 关键逻辑：条件性地添加 season 参数
        # 只有当 season 存在且不等于 "all" 时，才将其加入到请求参数中
        if season and season.lower() != "all":
            params["season"] = season
        
        # 发送请求
        # 此时的 params 可能是 {"id": 123} 或 {"id": 123, "season": "2023"}
        response = await client.get(f"{API_URL}/players/statistics", headers=HEADERS, params=params)
        
        # 检查响应状态
        response.raise_for_status()
        
        # 返回JSON数据
        return response.json()
    
async def get_team_roster(team_id: int, season: str):
    """
    获取单个球队在特定赛季的球员名单
    """
    async with httpx.AsyncClient() as client:
        params = {"team": team_id, "season": season}
        response = await client.get(f"{API_URL}/players", headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()
    
async def get_games_by_date(date: str):
    """
    获取指定日期的所有比赛
    """
    async with httpx.AsyncClient() as client:
        params = {"date": date}
        response = await client.get(f"{API_URL}/games", headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json()

