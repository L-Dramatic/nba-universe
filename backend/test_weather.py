#!/usr/bin/env python3
"""
快速测试天气API的诊断脚本
运行: python test_weather.py
"""

import asyncio
import sys
from pathlib import Path

# 添加app目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from app.core.config import WEATHER_API_KEY
from app.services import weather_service
from app.city_mapping import get_weather_city_name, CITY_WEATHER_MAPPING


async def test_weather():
    print("\n" + "="*70)
    print("🌤️  NBA Universe - 天气API诊断工具")
    print("="*70 + "\n")
    
    # 1. 检查API密钥
    print("📋 步骤1: 检查API配置")
    print("-" * 70)
    if not WEATHER_API_KEY:
        print("❌ ERROR: WEATHER_API_KEY 未配置!")
        print("   请在 backend/.env 文件中添加:")
        print("   WEATHER_API_KEY=your_api_key_here")
        print("\n   获取免费API密钥: https://openweathermap.org/api\n")
        return
    else:
        print(f"✅ API密钥已配置: {WEATHER_API_KEY[:8]}...{WEATHER_API_KEY[-4:]}")
    
    # 2. 显示映射表信息
    print(f"\n📊 步骤2: 城市映射表统计")
    print("-" * 70)
    print(f"✅ 已配置 {len(CITY_WEATHER_MAPPING)} 个城市映射")
    
    # 3. 测试常见NBA城市
    print(f"\n🧪 步骤3: 测试NBA球队城市")
    print("-" * 70)
    
    test_cities = [
        ("Los Angeles", "湖人/快船"),
        ("San Francisco", "勇士"),
        ("Boston", "凯尔特人"),
        ("New York", "尼克斯"),
        ("Brooklyn", "篮网"),
        ("Chicago", "公牛"),
        ("Miami", "热火"),
        ("Toronto", "猛龙"),
        ("Dallas", "独行侠"),
        ("Phoenix", "太阳"),
    ]
    
    success_count = 0
    fail_count = 0
    
    for city, team in test_cities:
        weather_city = get_weather_city_name(city)
        
        if not weather_city:
            print(f"❌ {city:20s} ({team:10s}) → 无法映射")
            fail_count += 1
            continue
        
        # 尝试获取天气
        weather_data = await weather_service.get_weather_by_city(weather_city)
        
        if weather_data and not isinstance(weather_data, Exception):
            temp = weather_data.get("main", {}).get("temp", "N/A")
            desc = weather_data.get("weather", [{}])[0].get("description", "N/A")
            print(f"✅ {city:20s} ({team:10s}) → {weather_city:25s} | {temp}°C, {desc}")
            success_count += 1
        else:
            print(f"❌ {city:20s} ({team:10s}) → {weather_city:25s} | API请求失败")
            fail_count += 1
        
        # 避免API限流
        await asyncio.sleep(0.2)
    
    # 4. 结果统计
    print(f"\n📈 步骤4: 测试结果统计")
    print("-" * 70)
    print(f"✅ 成功: {success_count}/{len(test_cities)}")
    print(f"❌ 失败: {fail_count}/{len(test_cities)}")
    
    if fail_count > 0:
        print("\n⚠️  建议:")
        print("  1. 检查网络连接")
        print("  2. 确认API密钥有效")
        print("  3. 检查是否触发API限流 (免费版: 60次/分钟)")
        print("  4. 查看详细日志: backend/WEATHER_DIAGNOSTIC_GUIDE.md")
    
    print("\n" + "="*70 + "\n")


if __name__ == "__main__":
    try:
        asyncio.run(test_weather())
    except KeyboardInterrupt:
        print("\n\n⏹️  测试已中断")
    except Exception as e:
        print(f"\n\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()


