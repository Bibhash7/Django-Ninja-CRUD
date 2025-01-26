from ninja import Schema
from typing import List, Optional
from datetime import datetime


class TrackSchema(Schema):
    title: Optional[str] = None
    artist: Optional[str] = None
    duration: Optional[float] = None
    last_play: Optional[datetime] = None

class SuccessSchema(Schema):
    Success: List[TrackSchema]
    
class ErrorSchema(Schema):
    Error: str
    