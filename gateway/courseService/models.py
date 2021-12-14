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
    category: Optional[str]


class CourseUpdate(BaseModel):
    name: Optional[str]
    owner: Optional[UUID]
    description: Optional[str]
    sub_level: Optional[int]
    latitude: Optional[float]
    longitude: Optional[float]
    category: Optional[str]
    hashtags: Optional[List[str]]


class ReviewCreate(BaseModel):
    description: Optional[str]
    rating: int


class ContentCreate(BaseModel):
    name: str
    link: str


class CourseFilter:
    def __init__(
        self,
        id: Optional[UUID] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        sub_level: Optional[int] = None,
        latitude: Optional[float] = None,
        longitude: Optional[float] = None,
        hashtag: Optional[str] = None,
        minRating: Optional[int] = None,
        category: Optional[str] = None
    ):
        self.id = id
        self.name = name
        self.description = description
        self.sub_level = sub_level
        self.latitude = latitude
        self.longitude = longitude
        self.hashtag = hashtag
        self.minRating = minRating
        self.category = category
