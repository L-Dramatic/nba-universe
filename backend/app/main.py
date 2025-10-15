# In backend/app/main.py

import asyncio
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import traceback

# 导入我们自己的服务和模块
from app.services import nba_service, news_service, weather_service, image_service, leaders_service
from app.services.leaders_service import get_nba_player_id_by_name
from app.data_loader import get_arena_coordinates

# --- App Initialization ---
app = FastAPI(
    title="NBA Universe API",
    description="An API that fuses NBA data with real-world information.",
    version="1.0.0"
)

# --- CORS Middleware ---
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API Endpoints ---

@app.get("/")
def read_root():
    """根路径，提供欢迎信息"""
    return {"message": "Welcome to the NBA Universe API"}


@app.get("/search")
async def search_players_and_teams(query: str = Query(..., min_length=3)):
    if len(query) < 3: return {"teams": [], "players": []}
    query_parts = query.split()
    player_search_term = query_parts[-1]
    try:
        team_results_task = nba_service.search_team_by_name(query)
        player_results_task = nba_service.search_player_by_name(player_search_term)
        team_results, player_results_raw = await asyncio.gather(team_results_task, player_results_task)
        filtered_players = []
        if player_results_raw.get("response") and len(query_parts) > 1:
            first_name_query = " ".join(query_parts[:-1]).lower()
            for player in player_results_raw["response"]:
                if player.get("firstname") and first_name_query in player["firstname"].lower():
                    filtered_players.append(player)
            if not filtered_players:
                filtered_players = player_results_raw.get("response", [])
        else:
            filtered_players = player_results_raw.get("response", [])
        
        # 为每个球员添加 NBA 官方 ID（用于头像）
        for player in filtered_players:
            if player.get("firstname") and player.get("lastname"):
                nba_official_id = get_nba_player_id_by_name(
                    player["firstname"], 
                    player["lastname"]
                )
                if nba_official_id:
                    player["nba_official_id"] = nba_official_id
        
        return {"teams": team_results.get("response", []), "players": filtered_players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/team-details/{team_name}")
async def get_team_details(team_name: str, season: str = Query("2023")):  # 免费 API 支持 2021-2023
    try:
        team_search_result = await nba_service.search_team_by_name(team_name)
        if not team_search_result or not team_search_result.get("response"):
            raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")
        
        team_info = team_search_result["response"][0]
        team_id, city, full_name, code = team_info["id"], team_info["city"], team_info["name"], team_info["code"]

        results = await asyncio.gather(
            nba_service.get_team_roster(team_id, season),
            news_service.get_news_by_keyword(full_name),
            weather_service.get_weather_by_city(city),
            image_service.get_image_url_by_keyword(city),
            return_exceptions=True
        )
        roster_data, news_data, weather_data, image_url = results
        arena_coords = get_arena_coordinates(code)

        return {
            "team_info": team_info,
            "city_context": {"weather": weather_data if not isinstance(weather_data, Exception) else None, "image_url": image_url if not isinstance(image_url, Exception) else None, "arena_coordinates": arena_coords},
            "roster": roster_data.get("response", []) if not isinstance(roster_data, Exception) else [],
            "news": news_data.get("articles", []) if not isinstance(news_data, Exception) else []
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.get("/player-details/{player_id}")
async def get_player_details(player_id: int, season: str = Query("2023")):  # 免费 API 支持 2021-2023
    try:
        print(f"\n=== Fetching player details: player_id={player_id}, season={season} ===")
        
        # 核心修复：先并发获取球员基本信息和统计数据
        # 这样即使统计数据为空，也能保证球员名字等基本信息正常显示
        player_basic_info_task = nba_service.get_player_by_id(player_id)
        player_stats_task = nba_service.get_player_statistics(player_id, season)
        
        player_basic_data, player_stats_data = await asyncio.gather(
            player_basic_info_task, 
            player_stats_task,
            return_exceptions=True
        )
        
        # 初始化返回数据
        player_info = {}
        avg_stats = {}
        
        # 1. 先处理球员基本信息（优先级最高，确保名字等信息一定能显示）
        if not isinstance(player_basic_data, Exception) and player_basic_data.get("response"):
            player_info = player_basic_data["response"][0]
            print(f"✓ Got basic info for: {player_info.get('firstname')} {player_info.get('lastname')}")
        else:
            print(f"✗ Failed to get basic info: {player_basic_data if isinstance(player_basic_data, Exception) else 'No response'}")
        
        # 2. 处理统计数据
        if not isinstance(player_stats_data, Exception):
            game_stats_list = player_stats_data.get("response", [])
            print(f"✓ Got stats data: {len(game_stats_list) if game_stats_list else 0} games")
            
            # 如果有统计数据，计算平均值
            if game_stats_list and len(game_stats_list) > 0:
                total_games, total_points, total_rebounds, total_assists, total_steals, total_blocks = 0, 0, 0, 0, 0, 0
                
                # 尝试从统计数据中更新球队信息（因为更准确，代表该赛季的球队）
                first_game = game_stats_list[0]
                if first_game.get("team"):
                    player_info['team'] = first_game["team"]
                
                # 计算该赛季平均数据
                for game in game_stats_list:
                    try:
                        # 更健壮的上场时间检查
                        min_played = game.get("min")
                        if min_played:
                            # 尝试转换为整数，如果失败则跳过这场比赛
                            if isinstance(min_played, str):
                                # 可能是 "30" 或 "00:30" 格式，取第一个数字部分
                                min_played = int(min_played.split(":")[0]) if ":" in min_played else int(min_played)
                            else:
                                min_played = int(min_played)
                            
                            # 只统计上场时间大于0的比赛
                            if min_played > 0:
                                total_games += 1
                                total_points += game.get("points") or 0
                                total_rebounds += game.get("totReb") or 0
                                total_assists += game.get("assists") or 0
                                total_steals += game.get("steals") or 0
                                total_blocks += game.get("blocks") or 0
                    except (ValueError, TypeError, AttributeError) as e:
                        # 某场比赛数据格式异常，跳过该场比赛
                        print(f"Warning: Skipping game due to data format issue: {e}")
                        continue
                
                if total_games > 0:
                    avg_stats = {
                        "games_played": total_games,
                        "points": round(total_points / total_games, 1),
                        "rebounds": round(total_rebounds / total_games, 1),
                        "assists": round(total_assists / total_games, 1),
                        "steals": round(total_steals / total_games, 1),
                        "blocks": round(total_blocks / total_games, 1)
                    }
                    print(f"✓ Calculated averages: {total_games} games, {avg_stats['points']} PPG")
                else:
                    print(f"✗ No valid games found (total_games = 0)")
            else:
                print(f"✗ No game stats available for season {season}")
        else:
            print(f"✗ Stats data request failed: {player_stats_data}")
        
        # 3. 获取 NBA 官方 ID（通过 nba_api）
        # 这个ID可以直接用于构建 NBA.com 的头像 URL
        if player_info.get("firstname") and player_info.get("lastname"):
            nba_official_id = get_nba_player_id_by_name(
                player_info['firstname'], 
                player_info['lastname']
            )
            if nba_official_id:
                player_info['nba_official_id'] = nba_official_id
        
        # 4. 获取新闻（如果有球员名字的话）
        news_data = {}
        if player_info.get("firstname") and player_info.get("lastname"):
            full_name = f"{player_info['firstname']} {player_info['lastname']}"
            news_data = await news_service.get_news_by_keyword(full_name)
        
        return {
            "player_info": player_info,
            "statistics": avg_stats,
            "news": news_data.get("articles", [])
        }
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

# --- 核心修复点：为 get_schedule 添加路由装饰器 ---
@app.get("/schedule/{date}")
async def get_schedule(date: str):
    """
    获取指定日期的比赛赛程。日期格式: YYYY-MM-DD。
    """
    try:
        games_data = await nba_service.get_games_by_date(date)
        return games_data.get("response", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get schedule: {str(e)}")
# --------------------------------------------------

@app.get("/leaders/{category}")
async def get_league_leaders(category: str, season: str = Query("2023")):
    valid_categories = {"points", "rebounds", "assists", "steals", "blocks"}
    if category.lower() not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category. Valid categories are: {', '.join(valid_categories)}")
    try:
        leaders_data = await leaders_service.get_league_leaders_from_nba_api(category, season)
        
        # 为每个球员添加 NBA 官方 ID（用于头像）
        for player in leaders_data[:20]:
            player_name = player.get("PLAYER", "")
            if player_name:
                # 分割名字（格式通常是 "First Last" 或 "First Middle Last"）
                name_parts = player_name.split()
                if len(name_parts) >= 2:
                    firstname = name_parts[0]
                    lastname = " ".join(name_parts[1:])  # 处理多个姓氏的情况
                    nba_official_id = get_nba_player_id_by_name(firstname, lastname)
                    if nba_official_id:
                        player["nba_official_id"] = nba_official_id
        
        return leaders_data[:20]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get league leaders: {str(e)}")

@app.get("/news/hot")
async def get_hot_news():
    """
    获取NBA热点新闻
    """
    try:
        news_data = await news_service.get_news_by_keyword("NBA")
        # 如果没有返回articles，返回空数组
        if not news_data or "articles" not in news_data:
            return {"articles": []}
        return news_data
    except Exception as e:
        print(f"Error fetching hot news: {e}")
        # 返回空数组而不是抛出异常
        return {"articles": []}