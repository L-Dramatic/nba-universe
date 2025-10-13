# in backend/app/data_loader.py
import json
import os

# 构建 arena_coordinates.json 文件的绝对路径
DATA_FILE_PATH = os.path.join(os.path.dirname(__file__), 'data', 'arena_coordinates.json')

def load_arena_data():
    try:
        with open(DATA_FILE_PATH, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

ARENA_DATA = load_arena_data()

def get_arena_coordinates(team_code: str):
    """
    通过球队代码 (e.g., 'LAL') 获取场馆坐标
    """
    return ARENA_DATA.get(team_code)