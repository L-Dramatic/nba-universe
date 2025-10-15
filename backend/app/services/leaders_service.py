import asyncio
from nba_api.stats.endpoints import leagueleaders
from nba_api.stats.static import players
from cachetools import TTLCache
import pandas as pd
import httpx

# 同样为榜单数据创建一个缓存
leaders_cache = TTLCache(maxsize=10, ttl=3600) # 缓存1小时

# 球员ID缓存（永久缓存，因为球员ID不会变）
player_id_cache = {}

# API-Sports ID 缓存（NBA官方ID -> API-Sports ID）
api_sports_id_cache = {}

def get_nba_player_id_by_name(firstname: str, lastname: str):
    """
    通过球员姓名获取 NBA 官方 ID
    这个 ID 可以直接用于构建 NBA.com 的头像 URL
    
    Args:
        firstname: 球员名字
        lastname: 球员姓氏
        
    Returns:
        NBA 官方球员 ID，如果找不到返回 None
    """
    cache_key = f"{firstname}_{lastname}"
    
    # 检查缓存
    if cache_key in player_id_cache:
        return player_id_cache[cache_key]
    
    try:
        # 获取所有球员列表（这个操作很快，nba_api 会缓存）
        all_players = players.get_players()
        
        # 搜索匹配的球员（不区分大小写）
        for player in all_players:
            if (player['first_name'].lower() == firstname.lower() and 
                player['last_name'].lower() == lastname.lower()):
                player_id = player['id']
                # 缓存结果
                player_id_cache[cache_key] = player_id
                print(f"✓ Found NBA official ID for {firstname} {lastname}: {player_id}")
                return player_id
        
        print(f"✗ No NBA official ID found for {firstname} {lastname}")
        return None
    except Exception as e:
        print(f"Error searching for player {firstname} {lastname}: {e}")
        return None

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