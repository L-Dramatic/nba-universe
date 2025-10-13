import asyncio
from nba_api.stats.endpoints import leagueleaders
from cachetools import TTLCache
import pandas as pd

# 同样为榜单数据创建一个缓存
leaders_cache = TTLCache(maxsize=10, ttl=3600) # 缓存1小时

def get_leaders_sync(category: str, season: str):
    """
    这是一个同步函数，它会执行耗时的API调用。
    """
    print(f"正在从nba_api获取 {season} 赛季 {category} 榜单...")
    # nba_api的category需要首字母大写
    category_map = {
        "points": "PTS",
        "rebounds": "REB",
        "assists": "AST",
        "steals": "STL",
        "blocks": "BLK",
    }
    
    # 确保我们使用的是nba_api期望的赛季格式，例如 '2023-24'
    season_formatted = f"{season}-{str(int(season) + 1)[-2:]}"

    try:
        leaders = leagueleaders.LeagueLeaders(
            season=season_formatted,
            per_mode48="PerGame",
            stat_category_abbreviation=category_map.get(category.lower(), "PTS")
        )
        # 将结果转换为更易于处理的 a list of dictionaries
        df = leaders.get_data_frames()[0]
        return df.to_dict('records')
    except Exception as e:
        print(f"nba_api调用失败: {e}")
        return []

async def get_league_leaders_from_nba_api(category: str, season: str):
    """
    这是我们将从main.py调用的异步函数。
    """
    cache_key = f"leaders_{season}_{category}"
    if cache_key in leaders_cache:
        print(f"从缓存中获取榜单: {cache_key}")
        return leaders_cache[cache_key]

    # 在异步应用中调用同步代码的最佳方式是使用 run_in_executor
    loop = asyncio.get_running_loop()
    # 这会在一个单独的线程中运行同步函数，防止阻塞
    result = await loop.run_in_executor(
        None, get_leaders_sync, category, season
    )
    
    leaders_cache[cache_key] = result
    print(f"已获取并缓存榜单数据: {cache_key}")
    return result