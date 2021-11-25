from pydantic import BaseModel
from uuid import UUID
from typing import List, Optional


class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    hashtags: Optional[List] = []
    sub_level: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]


class CourseUpdate(BaseModel):
    name: Optional[str]
    owner: Optional[UUID]
    description: Optional[str]
    sub_level: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]


class CourseFilter:
    def __init__(
        self,
        name: Optional[str] = None,
        owner: Optional[UUID] = None,
        description: Optional[str] = None,
        sub_level: Optional[int] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None
    ):
        self.name = name
        self.owner = owner
        self.description = description
        self.sub_level = sub_level
        self.latitude = latitude
        self.longitude = longitude
