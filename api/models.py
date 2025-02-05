from pydantic import BaseModel
from typing import List
from datetime import datetime

# Medalist Schema (used for inserting/fetching data)
class Medalist(BaseModel):
    name: str
    medal_type: str  # e.g., "Gold Medal" instead of just "Gold"
    gender: str
    country_code: str
    country: str
    country_long: Optional[str]  # Some records have this field
    nationality: str
    medal_code: int  # Previously a string, now an integer
    medal_date: datetime 
    discipline: str
    event: str
    event_type: Optional[str]  # Some records have this field
    url_event: Optional[str]  # Required for URL linking
    birth_date: Optional[str]  # Some records contain athlete birth dates
    code_athlete: Optional[int]  # Unique athlete identifier
    code_team: Optional[int]  # Team identifier, sometimes NaN
    team: Optional[str]  # Some records contain team names
    team_gender: Optional[str]  # Some records contain team gender

class EventAggregate(BaseModel):
    discipline: str
    event: str
    event_date: datetime
    medalists: List[Medalist]