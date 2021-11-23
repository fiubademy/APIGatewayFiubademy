import requests
from uuid import UUID, uuid4
from fastapi import Depends, APIRouter
from typing import List
from starlette.responses import JSONResponse
from sqlalchemy.orm import sessionmaker
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from courseService.models import CourseCreate, CourseUpdate, CourseFilter


URL_API = 'https://api-cursos-fiubademy.herokuapp.com/courses'
SESSION_EXPIRATION_TIME_IN_MINUTES = 30

router = APIRouter()
session = None
engine = None


def set_engine(engine_rcvd):
    global engine
    global session
    engine = engine_rcvd
    session = sessionmaker(bind=engine)()


@router.get('/all/{page_num}')
async def get_courses(
    page_num: int,
    filter: CourseFilter = Depends()
):
    query = requests.get(f'{URL_API}/all/{page_num}', params=filter.__dict__)
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.get('/{courseId}')
async def get_by_id(courseId):
    query = requests.get(f'{URL_API}/{courseId}')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/student/{userId}')
async def get_by_student(userId: UUID):
    url_request = f'{URL_API}/student/{userId}'
    query = requests.get(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/collaborator/{userId}')
async def get_by_collaborator(userId: UUID):
    url_request = f'{URL_API}/student/{userId}'
    query = requests.get(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('')
async def create(request: CourseCreate):
    url_request = URL_API
    query = requests.post(url_request, data=request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/{courseId}')
async def delete(courseId: UUID):
    url_request = f'{URL_API}/{courseId}'
    query = requests.delete(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.patch('/{courseId}')
async def update(courseId: UUID, request: CourseUpdate):
    url_request = f'{URL_API}/{courseId}'
    query = requests.patch(url_request, data=request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/{courseId}/students')
async def get_students(courseId: UUID):
    url_request = f'{URL_API}/{courseId}/students'
    query = requests.get(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/{courseId}/add_student/{userId}')
async def add_student(courseId: UUID, userId: UUID):
    url_request = f'{URL_API}/{courseId}/add_student/{userId}'
    query = requests.post(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/{courseId}/remove_student/{userId}')
async def remove_student(courseId: UUID, userId: UUID):
    url_request = f'{URL_API}/{courseId}/remove_student/{userId}'
    query = requests.delete(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/{courseId}/collaborators')
async def get_collaborators(courseId: UUID):
    url_request = f'{URL_API}/{courseId}/collaborators'
    query = requests.get(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/{courseId}/add_collaborator/{userId}')
async def add_collaborator(courseId: UUID, userId: UUID):
    url_request = f'{URL_API}/{courseId}/add_collaborator/{userId}'
    query = requests.post(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/{courseId}/remove_collaborator/{userId}')
async def remove_collaborator(courseId: UUID, userId: UUID):
    url_request = f'{URL_API}/{courseId}/remove_collaborator/{userId}'
    query = requests.delete(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/{courseId}/hashtags')
async def get_hashtags(courseId: UUID):
    url_request = f'{URL_API}/{courseId}/hashtags'
    query = requests.get(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/{courseId}/add_hashtags')
async def add_hashtags(courseId: UUID, tags: List[str]):
    url_request = f'{URL_API}/{courseId}/add_hashtags'
    query = requests.post(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/{courseId}/remove_hashtags')
async def remove_hashtags(courseId: UUID, tags: List[str]):
    url_request = f'{URL_API}/{courseId}/remove_hashtags'
    query = requests.delete(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/hashtag/{tag}')
async def get_by_hashtag(tag: str):
    url_request = f'{URL_API}/hashtag/{tag}'
    query = requests.get(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/{courseId}/owner')
async def get_owner(courseId: UUID):
    url_request = f'{URL_API}/{courseId}/owner'
    query = requests.get(url_request)
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.put('/{courseId}/block')
async def set_block(courseId: UUID, block: bool = True):
    url_request = f'{URL_API}/{courseId}/block'
    query = requests.put(url_request, params={'block': str(block)})
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.put('/{courseId}/status')
async def set_status(courseId: UUID, in_edition: bool):
    url_request = f'{URL_API}/{courseId}/status'
    query = requests.put(url_request, params={'in_edition': str(in_edition)})
    return JSONResponse(status_code=query.status_code, content=query.json())
