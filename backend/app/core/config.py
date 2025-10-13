import os
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()

# 从环境变量中获取API密钥
NBA_API_KEY = os.getenv("NBA_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
UNSPLASH_API_KEY = os.getenv("UNSPLASH_API_KEY")

# 检查密钥是否成功加载 (可选，但推荐)
if not NBA_API_KEY:
    raise ValueError("NBA_API_KEY not found in .env file")