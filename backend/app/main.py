# In backend/app/main.py

import asyncio
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import traceback

# 导入我们自己的服务和模块
from app.services import nba_service, news_service, weather_service, image_service, leaders_service
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
        return {"teams": team_results.get("response", []), "players": filtered_players}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/team-details/{team_name}")
async def get_team_details(team_name: str, season: str = Query("2023")):
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
async def get_player_details(player_id: int, season: str = Query("2023")):
    try:
        player_stats_data = await nba_service.get_player_statistics(player_id, season)
        game_stats_list = player_stats_data.get("response")
        avg_stats, player_info, team_info = {}, {}, {}
        if game_stats_list:
            total_games, total_points, total_rebounds, total_assists, total_steals, total_blocks = 0, 0, 0, 0, 0, 0
            for game in game_stats_list:
                if game.get("min") and int(game["min"]) > 0:
                    total_games += 1; total_points += game.get("points") or 0; total_rebounds += game.get("totReb") or 0; total_assists += game.get("assists") or 0; total_steals += game.get("steals") or 0; total_blocks += game.get("blocks") or 0
            avg_stats = { "games_played": total_games, "points": round(total_points / total_games, 1) if total_games > 0 else 0, "rebounds": round(total_rebounds / total_games, 1) if total_games > 0 else 0, "assists": round(total_assists / total_games, 1) if total_games > 0 else 0, "steals": round(total_steals / total_games, 1) if total_games > 0 else 0, "blocks": round(total_blocks / total_games, 1) if total_games > 0 else 0 }
            player_info = game_stats_list[0].get("player", {}); team_info = game_stats_list[0].get("team", {})
        else:
            # 修复：当没有统计数据时，通过ID获取球员基本信息
            player_info_data = await nba_service.get_player_by_id(player_id)
            if player_info_data.get("response"):
                player_info = player_info_data["response"][0]
        # 修复：只有当有球队信息时才赋值，避免覆盖球员原有的球队信息
        if team_info:
            player_info['team'] = team_info
        news_data = {}
        if player_info.get("firstname") and player_info.get("lastname"):
            full_name = f"{player_info['firstname']} {player_info['lastname']}"
            news_data = await news_service.get_news_by_keyword(full_name)
        return {"player_info": player_info, "statistics": avg_stats, "news": news_data.get("articles", [])}
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
async def get_league_leaders(category: str):
    valid_categories = {"points", "rebounds", "assists", "steals", "blocks"}
    if category.lower() not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category. Valid categories are: {', '.join(valid_categories)}")
    try:
        season = "2023"
        leaders_data = await leaders_service.get_league_leaders_from_nba_api(category, season)
        return leaders_data[:20]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get league leaders: {str(e)}")