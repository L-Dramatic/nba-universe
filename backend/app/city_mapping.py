# City name mapping for weather API
# Maps NBA API city names to OpenWeatherMap-compatible city names

CITY_WEATHER_MAPPING = {
    # 主要城市直接映射
    "Los Angeles": "Los Angeles,US",
    "LA": "Los Angeles,US",  # 快船队使用缩写 "LA"
    "New York": "New York,US",
    "Chicago": "Chicago,US",
    "Houston": "Houston,US",
    "Phoenix": "Phoenix,US",
    "Philadelphia": "Philadelphia,US",
    "San Antonio": "San Antonio,US",
    "Dallas": "Dallas,US",
    "San Francisco": "San Francisco,US",
    "Boston": "Boston,US",
    "Miami": "Miami,US",
    "Atlanta": "Atlanta,US",
    "Denver": "Denver,US",
    "Seattle": "Seattle,US",
    "Detroit": "Detroit,US",
    "Washington": "Washington,US",
    "Milwaukee": "Milwaukee,US",
    "Minneapolis": "Minneapolis,US",
    "Cleveland": "Cleveland,US",
    "Memphis": "Memphis,US",
    "Charlotte": "Charlotte,US",
    "Indianapolis": "Indianapolis,US",
    "Portland": "Portland,US",
    "Sacramento": "Sacramento,US",
    "Orlando": "Orlando,US",
    "Salt Lake City": "Salt Lake City,US",
    "Oklahoma City": "Oklahoma City,US",
    "New Orleans": "New Orleans,US",
    
    # 特殊映射
    "Brooklyn": "New York,US",  # 布鲁克林使用纽约天气
    "Toronto": "Toronto,CA",     # 加拿大多伦多
    
    # 城市缩写映射
    "SF": "San Francisco,US",    # 勇士队可能使用 "SF"
    "NY": "New York,US",         # 尼克斯可能使用 "NY"
    "OKC": "Oklahoma City,US",   # 雷霆队常用 "OKC"
    "SLC": "Salt Lake City,US",  # 爵士队可能使用 "SLC"
    
    # 空值处理
    "": None,
    None: None
}

def get_weather_city_name(city: str) -> str:
    """
    将NBA API返回的城市名转换为OpenWeatherMap API兼容的格式
    
    Args:
        city: NBA API返回的城市名
        
    Returns:
        OpenWeatherMap API兼容的城市名，如果找不到返回原始值
    """
    if not city:
        return None
    
    # 去除首尾空格并标准化
    city = city.strip()
    
    # 先查找映射表（精确匹配）
    mapped_city = CITY_WEATHER_MAPPING.get(city)
    if mapped_city:
        return mapped_city
    
    # 大小写不敏感查找
    city_lower = city.lower()
    for key, value in CITY_WEATHER_MAPPING.items():
        if key and key.lower() == city_lower:
            print(f"[City Mapping] Found case-insensitive match: '{city}' -> '{value}'")
            return value
    
    # 如果没有映射，默认添加 ,US 后缀
    print(f"[City Mapping] No mapping found for '{city}', using default: '{city},US'")
    return f"{city},US"


