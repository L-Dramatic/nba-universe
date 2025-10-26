# 🏀 NBA Universe - Mashup Web Application

> **Course Project**: Microservice Architecture  
> **Student**: Li Xingshuo
> **Project Type**: Mashup-based Application  

---

## 📋 Project Overview

NBA Universe is a **mashup web application** that integrates information from **5 different API providers** to create a comprehensive, one-stop platform for NBA fans. By fusing sports data with real-world contextual information (weather, news, images), this application demonstrates the power of API integration and data mashup techniques.

**Key Innovation**: Unlike traditional sports websites that only display game statistics, NBA Universe enriches the user experience by combining NBA data with city weather conditions, news updates, visual content, and official player information—all presented in a modern, responsive interface.

---

## ✅ Course Requirements Compliance

This project satisfies **Constraint (1)** of the assignment requirements:

> *"Integrate information about a single specific topic or domain from at least four different providers and fuse it into a single application."*

### Integrated API Providers (5 total):

| # | API Provider | Purpose | Data Provided |
|---|-------------|---------|---------------|
| 1 | **API-Sports (NBA API)** | Core NBA data | Teams, players, rosters, game schedules, player statistics |
| 2 | **OpenWeatherMap API** | Weather information | Current weather, 24-hour forecast, air quality (3 different endpoints) |
| 3 | **NewsAPI** | Real-time news | Latest NBA news articles, team/player updates |
| 4 | **Unsplash API** | Visual content | High-quality city background images |
| 5 | **nba_api (Official NBA Stats)** | Official player data | Official player IDs, league leaderboards |

**Data Fusion Example**: When viewing a team's detail page, the application simultaneously displays:
- Team roster and player statistics (API-Sports)
- Current weather + forecast + air quality in the team's city (OpenWeatherMap - 3 API calls)
- Latest news about the team (NewsAPI)
- Beautiful cityscape photo (Unsplash)
- Official player headshots (nba_api)

---

## 🎯 Core Features

### 1. **Multi-Dimensional Search** 🔍
- Search for NBA teams and players simultaneously
- Real-time filtering with responsive UI
- Navigate to detailed team or player pages

### 2. **Rich Team Information** 🏀
- **Team Details**: City, conference, division, logo
- **Weather Context**: 
  - Current temperature, humidity, wind speed, visibility
  - 24-hour weather forecast (4 time periods)
  - Air Quality Index (AQI) with PM2.5 concentration
  - Sunrise/sunset times
- **Team Roster**: Complete player list with official headshots
- **News Feed**: Latest articles about the team
- **Visual Appeal**: City background images

### 3. **Comprehensive Player Profiles** 👤
- Player basic information (height, weight, position)
- Season statistics (points, rebounds, assists, steals, blocks per game)
- Career data across multiple seasons
- Related news articles
- Official NBA headshots

### 4. **Game Schedule** 📅
- View games by date
- Real-time game status
- Team matchups with logos

### 5. **League Leaders** 🏆
- Top 20 players by category:
  - Points per game
  - Rebounds per game
  - Assists per game
  - Steals per game
  - Blocks per game
- Official player rankings from NBA.com

### 6. **News Center** 📰
- Latest NBA news from multiple sources
- Article previews with images
- Direct links to full articles

---

## 🛠️ Technical Architecture

### **Backend** (Python + FastAPI)

**Framework**: FastAPI with async/await support

**Key Technologies**:
- `httpx`: Asynchronous HTTP client for API requests
- `asyncio`: Concurrent API calls for performance optimization
- `cachetools`: In-memory caching to reduce redundant API calls
- `pandas`: Data processing for league statistics
- `python-dotenv`: Environment variable management

**Architecture Highlights**:
```
Frontend Request
    ↓
FastAPI Gateway (Port 8000)
    ↓
Concurrent API Calls (asyncio.gather)
    ↓
┌─────────────────────────────────────────┐
│ API-Sports | NewsAPI | OpenWeatherMap  │
│ Unsplash   | nba_api                    │
└─────────────────────────────────────────┘
    ↓
Data Fusion & Processing
    ↓
Unified JSON Response
    ↓
Frontend Rendering
```

### **Frontend** (Vue 3 + Vite)

**Framework**: Vue 3 with Composition API

**Key Technologies**:
- `Vue Router`: Client-side routing
- `Pinia`: State management for API data caching
- `Axios`: HTTP client for backend communication
- `Tailwind CSS`: Utility-first CSS framework
- `Vite`: Next-generation build tool

**UI/UX Features**:
- Responsive design (mobile + desktop)
- Loading states and error handling
- Smooth animations and transitions
- Card-based layouts
- Dynamic backgrounds

---

## 📦 Installation & Deployment

### Prerequisites
- **Node.js** v18+ ([Download](https://nodejs.org/))
- **Python** 3.8+ ([Download](https://www.python.org/))

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys (see Configuration section below)
# Create a .env file with your API keys

# Start backend server
uvicorn app.main:app --reload
```

Backend will run at: `http://127.0.0.1:8000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

---

## ⚙️ Configuration

Create a `.env` file in the `backend/` directory with the following API keys:

```env
# Required API Keys
NBA_API_KEY=your_api_sports_key_here
NEWS_API_KEY=your_newsapi_key_here
WEATHER_API_KEY=your_openweathermap_key_here
UNSPLASH_API_KEY=your_unsplash_key_here
```

### How to Obtain API Keys:

1. **API-Sports (NBA API)**: 
   - Register at: https://api-sports.io/
   - Free tier: 100 requests/day
   - Documentation: https://api-sports.io/documentation/nba/v2

2. **NewsAPI**:
   - Register at: https://newsapi.org/
   - Free tier: 100 requests/day
   - Documentation: https://newsapi.org/docs

3. **OpenWeatherMap**:
   - Register at: https://openweathermap.org/api
   - Free tier: 60 calls/minute, 1M calls/month
   - Documentation: https://openweathermap.org/api

4. **Unsplash**:
   - Register at: https://unsplash.com/developers
   - Free tier: 50 requests/hour
   - Documentation: https://unsplash.com/documentation

5. **nba_api** (No API key required):
   - Python library: https://github.com/swar/nba_api
   - Direct access to NBA.com stats

---

## 🌟 API Integration Details

### 1. API-Sports (NBA API)
**Base URL**: `https://v2.nba.api-sports.io`

**Endpoints Used**:
- `GET /teams` - Search teams by name
- `GET /players` - Search players and get player info
- `GET /players/statistics` - Get player statistics by season
- `GET /games` - Get game schedules by date

**Example Response Integration**:
```json
{
  "team_info": { "id": 13, "name": "Los Angeles Lakers", "logo": "..." },
  "roster": [
    { "id": 265, "firstname": "LeBron", "lastname": "James", ... }
  ]
}
```

### 2. OpenWeatherMap API (3 Endpoints)
**Base URL**: `https://api.openweathermap.org/data/2.5`

**Endpoints Used**:
- `GET /weather` - Current weather data
- `GET /forecast` - 5-day / 3-hour forecast
- `GET /air_pollution` - Air quality index

**Data Fusion**:
```json
{
  "current": { "temp": 22.5, "humidity": 65, "wind": { "speed": 3.5 } },
  "forecast": { "list": [...] },
  "air_quality": { "main": { "aqi": 2 }, "components": { "pm2_5": 12.5 } }
}
```

### 3. NewsAPI
**Base URL**: `https://newsapi.org/v2`

**Endpoint Used**:
- `GET /everything` - Search news articles by keyword

**Integration**: Searches for team/player names to fetch relevant news

### 4. Unsplash API
**Base URL**: `https://api.unsplash.com`

**Endpoint Used**:
- `GET /search/photos` - Search photos by city name

**Integration**: Fetches high-quality city images for team detail pages

### 5. nba_api (Python Library)
**Source**: Official NBA.com statistics

**Functions Used**:
- `leagueLeaders.LeagueLeaders()` - Get league leader statistics
- `players.find_players_by_full_name()` - Match player names to official IDs

**Integration**: Provides official player IDs for headshot URLs and league rankings

---

## 📂 Project Structure

```
nba-universe/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   └── config.py              # API key configuration
│   │   ├── services/
│   │   │   ├── nba_service.py         # API-Sports integration
│   │   │   ├── weather_service.py     # OpenWeatherMap integration (3 endpoints)
│   │   │   ├── news_service.py        # NewsAPI integration
│   │   │   ├── image_service.py       # Unsplash integration
│   │   │   └── leaders_service.py     # nba_api integration
│   │   ├── data/
│   │   │   └── arena_coordinates.json # Static arena location data
│   │   ├── city_mapping.py            # City name normalization
│   │   ├── data_loader.py             # Static data loader
│   │   ├── main.py                    # FastAPI application & endpoints
│   │   └── models.py                  # Pydantic data models
│   ├── requirements.txt               # Python dependencies
│   └── .env                           # API keys (not in git)
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── client.js              # Axios backend client
│   │   ├── components/
│   │   │   ├── nba/
│   │   │   │   ├── PlayerCard.vue     # Player display component
│   │   │   │   ├── WeatherCard.vue    # Weather display component
│   │   │   │   ├── NewsListItem.vue   # News item component
│   │   │   │   └── StatBox.vue        # Statistics box component
│   │   │   └── ui/
│   │   │       ├── LoadingSpinner.vue
│   │   │       └── ErrorMessage.vue
│   │   ├── views/
│   │   │   ├── Home.vue               # Search page
│   │   │   ├── TeamDetail.vue         # Team detail page
│   │   │   ├── PlayerDetail.vue       # Player detail page
│   │   │   ├── Schedule.vue           # Game schedule page
│   │   │   ├── Leaders.vue            # League leaders page
│   │   │   └── News.vue               # News page
│   │   ├── stores/
│   │   │   └── nbaStore.js            # Pinia state management
│   │   ├── router/
│   │   │   └── index.js               # Vue Router configuration
│   │   ├── App.vue                    # Root component
│   │   └── main.js                    # Application entry point
│   ├── package.json                   # Node dependencies
│   └── vite.config.js                 # Vite configuration
└── README.md                          # This file
```

---

## 🎨 User Interface Highlights

### Modern Design Principles
- **Gradient backgrounds**: Blue theme matching NBA aesthetics
- **Card-based layouts**: Information organized in digestible cards
- **Responsive grid system**: Adapts from mobile to desktop
- **Loading states**: Spinner animations during API calls
- **Error handling**: User-friendly error messages
- **Smooth transitions**: CSS animations for better UX

### Key Pages

1. **Home/Search Page**:
   - Prominent search bar with NBA background
   - Real-time search results (teams + players)
   - Quick navigation to detail pages

2. **Team Detail Page**:
   - Hero banner with team logo and city image
   - Comprehensive weather card (current + forecast + AQI)
   - Interactive roster grid with player cards
   - News feed with load-more functionality

3. **Player Detail Page**:
   - Official player headshot
   - Season statistics dashboard
   - Career data display
   - Related news section

4. **Schedule Page**:
   - Date selector for game schedules
   - Game cards showing matchups
   - Real-time game status

5. **Leaders Page**:
   - Category tabs (Points, Rebounds, Assists, etc.)
   - Top 20 player rankings
   - Official statistics from NBA.com

---

## 🔬 Technical Highlights

### 1. Asynchronous API Calls
```python
# Concurrent API requests for better performance
results = await asyncio.gather(
    nba_service.get_team_roster(team_id, season),
    news_service.get_news_by_keyword(team_name),
    weather_service.get_comprehensive_weather(city),
    image_service.get_image_url_by_keyword(city),
    return_exceptions=True  # Graceful error handling
)
```

### 2. Data Normalization
```python
# City name mapping for weather API compatibility
CITY_WEATHER_MAPPING = {
    "LA": "Los Angeles,US",           # Clippers use "LA"
    "Brooklyn": "New York,US",        # Brooklyn uses NYC weather
    "Toronto": "Toronto,CA",          # Canadian city
    # ... 30+ NBA cities mapped
}
```

### 3. Multi-Endpoint Weather Integration
```python
# Calling 3 different OpenWeatherMap endpoints
async def get_comprehensive_weather(city: str):
    current = await get_weather_by_city(city)       # Current Weather API
    forecast = await get_weather_forecast(city)     # Forecast API
    air_quality = await get_air_quality(lat, lon)   # Air Pollution API
    
    return {
        "current": current,
        "forecast": forecast,
        "air_quality": air_quality
    }
```

### 4. State Management with Pinia
```javascript
// Centralized API call management with caching
export const useNbaStore = defineStore('nba', {
  state: () => ({
    teamDetailsCache: {},  // Avoid redundant API calls
    searchResults: null,
    // ...
  }),
  actions: {
    async fetchTeamDetails(teamName, season) {
      const cacheKey = `${teamName}_${season}`;
      if (this.teamDetailsCache[cacheKey]) {
        return this.teamDetailsCache[cacheKey];
      }
      // Make API call and cache result
    }
  }
});
```

---

## 🧪 Testing the Application

### Quick Test Checklist

1. **Search Functionality**:
   - Search for "Lakers" → Should show Los Angeles Lakers team and players
   - Search for "LeBron James" → Should show LeBron in player results

2. **Team Detail Page**:
   - Click on "Los Angeles Lakers" → Should display:
     - ✅ Team logo and city background image
     - ✅ Current weather in Los Angeles (temp, humidity, wind)
     - ✅ 24-hour forecast with weather icons
     - ✅ Air quality index
     - ✅ Complete roster with player photos
     - ✅ Latest Lakers news articles

3. **Player Detail Page**:
   - Click on any player → Should display:
     - ✅ Player headshot (official NBA.com image)
     - ✅ Season statistics (PPG, RPG, APG, SPG, BPG)
     - ✅ Related news articles

4. **Schedule Page**:
   - Select a date → Should show games for that day

5. **Leaders Page**:
   - Click "Points" → Should show top 20 scorers
   - Click "Rebounds" → Should show top 20 rebounders
   - Each player should have official headshot

6. **News Page**:
   - Should display latest NBA news articles

---

## 📊 API Usage Statistics

| Feature | API Calls per Page Load |
|---------|------------------------|
| Search Results | 2 (teams + players) |
| Team Detail Page | 5 (roster + weather×3 + news + image) |
| Player Detail Page | 3 (player info + stats + news) |
| Schedule Page | 1 (games by date) |
| Leaders Page | 1 (leaderboard data) |
| News Page | 1 (hot news) |

**Performance Optimization**:
- Frontend caching with Pinia (avoid duplicate requests)
- Backend async concurrency (parallel API calls)
- Error resilience (one API failure doesn't crash the page)

---

## 🎓 Learning Outcomes

Through this project, I demonstrated proficiency in:

1. **API Integration**: Successfully integrated 5 different API providers with varying authentication methods and response formats
2. **Data Fusion**: Combined heterogeneous data sources into a cohesive user experience
3. **Asynchronous Programming**: Utilized Python's `asyncio` for concurrent API requests
4. **Modern Web Development**: Built a full-stack application with FastAPI and Vue 3
5. **Error Handling**: Implemented graceful degradation when APIs fail
6. **State Management**: Used Pinia for efficient data caching and sharing
7. **Responsive Design**: Created a mobile-friendly interface with Tailwind CSS

---

## 📚 API Documentation Links

- **API-Sports (NBA)**: https://api-sports.io/documentation/nba/v2
- **OpenWeatherMap**: 
  - Current Weather: https://openweathermap.org/current
  - Forecast: https://openweathermap.org/forecast5
  - Air Pollution: https://openweathermap.org/api/air-pollution
- **NewsAPI**: https://newsapi.org/docs/endpoints/everything
- **Unsplash**: https://unsplash.com/documentation
- **nba_api**: https://github.com/swar/nba_api

---

## 🚀 Future Enhancements

Potential improvements for future iterations:

1. **User Authentication**: Allow users to save favorite teams/players
2. **Real-time Updates**: WebSocket integration for live game scores
3. **Advanced Analytics**: Statistical visualizations and player comparisons
4. **Social Features**: User comments and discussions
5. **Caching Layer**: Redis for persistent caching across server restarts
6. **Mobile App**: React Native version for iOS/Android

---

## 📝 License

This project is developed for educational purposes as part of the Microservice Architecture course.

---

## 👨‍💻 Author

**[Li Xingshuo]**  
Microservice Architecture Course Project  
[Tongji University]  
Submission Date: October 27, 2025