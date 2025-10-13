# in backend/app/models.py
from pydantic import BaseModel, Field
from typing import List, Optional, Any

# 这是一个示例，你可以根据需要扩展
class TeamInfo(BaseModel):
    id: int
    name: str
    logo: Optional[str] = None
    city: str

class PlayerInfo(BaseModel):
    id: int
    name: str
    team: Optional[str] = None

class SearchResult(BaseModel):
    teams: List[TeamInfo]
    players: List[PlayerInfo]
