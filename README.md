# 🏀 NBA Universe - 集成体育数据中心

欢迎来到 NBA Universe！这是一个为《微服务架构》课程设计的个人项目，旨在构建一个功能丰富的“混搭式”(Mashup) Web应用程序。本项目通过集成多个独立的Web API，为NBA球迷提供一个一站式、多维度的数据探索平台。

![项目首页截图](URL_TO_YOUR_PROJECT_SCREENSHOT_1)
*(提示：项目完成后，你可以在这里替换成一张真实的项目截图)*

---

## ✨ 项目亮点与特色

与传统的体育数据网站不同，NBA Universe 的核心特色在于**数据融合**，它不仅展示了球员和球队的比赛数据，更将这些数据与现实世界的背景信息相结合，创造出独特的沉浸式体验：

- **多维度信息聚合**: 一站式查看球队阵容、赛程、球员生涯数据、联盟排行榜等核心信息。
- **城市背景融合**: 在查看球队详情时，可以同时了解该球队主场城市的实时天气、在交互式地图上查看球馆位置，并欣赏精美的城市风光照片。
- **实时动态**: 集成了最新的NBA新闻源，让你随时掌握联盟、球队和球员的动态。
- **现代化的UI/UX**: 采用响应式设计，无论是桌面还是移动设备都能获得良好体验。界面设计注重视觉效果，使用了动态背景、过渡动画和卡片式布局。

---

## 🛠️ 技术架构

本项目采用现代Web开发中流行的**前后端分离**架构。

### 后端 (Backend)

- **框架**: **Python 3 + FastAPI**
  - 利用FastAPI的高性能和异步特性，构建了一个API网关，负责从多个外部数据源并发请求数据，并将它们聚合成统一的、干净的JSON格式返回给前端。
- **核心功能**:
  - API数据聚合与融合。
  - 部分复杂数据的后端计算（如赛季平均数据、球员榜单排序）。
  - 使用内存缓存 (`cachetools`) 优化对高频或不常变化数据的请求。
- **数据源 (API集成)**:
  1. **API-Sports (NBA API)**: 提供核心的NBA比赛、球员、球队数据。
  2. **NewsAPI**: 提供实时新闻文章。
  3. **OpenWeatherMap**: 提供城市天气数据。
  4. **Mapbox**: 提供地理编码服务，将地址转换为坐标。
  5. **Unsplash**: 提供高质量的城市背景图片。
  6. **`nba_api` (Python库)**: 作为补充，用于获取官方处理好的联盟球员榜单数据。

### 前端 (Frontend)

- **框架**: **Vue 3** (使用 Composition API 和 `<script setup>` 语法)
- **构建工具**: **Vite**
- **核心技术**:
  - **Vue Router**: 管理应用的页面导航（路由）。
  - **Pinia**: 作为中央状态管理器，统一处理所有API请求的发起、数据缓存和状态共享。
  - **Axios**: 用于与后端API进行HTTP通信。
  - **Tailwind CSS**: 一个功能优先的CSS框架，用于快速构建现代化、响应式的用户界面。

---

## 🚀 本地运行指南

请确保你已安装 [Node.js](https://nodejs.org/) (v18+) 和 [Python](https://www.python.org/) (v3.8+)。

### 1. 准备工作

克隆本项目并进入目录：
```bash
git clone https://github.com/YourUsername/nba-universe.git
cd nba-universe
```

### 2. 启动后端服务

首先，我们需要启动后端API服务器。

```bash
# 1. 进入后端目录
cd backend

# 2. 创建并激活Python虚拟环境
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# Mac/Linux: source .venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置API密钥
#    复制 .env.example 为 .env，并填入你的密钥
cp .env.example .env

# 5. 启动服务
uvicorn app.main:app --reload
```
> 👉 后端服务将运行在 `http://127.0.0.1:8000`。

### 3. 启动前端应用

在**新的终端窗口**中，启动前端开发服务器。

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动服务
npm run dev
```
> 👉 前端应用将运行在 `http://localhost:5173`。

现在，打开浏览器访问 `http://localhost:5173` 即可开始使用！

---

## 📄 课程要求满足情况

本项目严格遵守了课程要求中的**约束条件 (1)**：

> 集成关于**某个特定主题或领域**（NBA篮球）的信息，这些信息来自**至少四个不同的提供商**（本项目集成了六个），并将其**融合到一个单一的应用程序**中。