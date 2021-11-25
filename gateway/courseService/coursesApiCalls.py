from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from typing import List
from fastapi import Depends, APIRouter, status
from uuid import UUID
import requests

from courseService.models import CourseCreate, CourseUpdate, CourseFilter
from courseService.validations import admin_access, validate_session_token, owner_access, student_access, teacher_access, validate_subscription
from courseService.setupCourseApi import URL_API

router = APIRouter(dependencies=[Depends(validate_session_token)])


@router.get('/all/{page_num}')
async def get_courses(
    page_num: int,
    filter: CourseFilter = Depends()
):
    url_request = f'{URL_API}/all/{page_num}'
    query = requests.get(url_request, params=filter.__dict__)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@router.get('/id/{courseId}')
async def get_by_id(courseId: UUID):
    url_request = f'{URL_API}/{courseId}'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/student/{userId}')
async def get_by_student(userId: UUID, _=Depends(admin_access)):
    # solo un admin puede ver los cursos de cada estudiante
    url_request = f'{URL_API}/student/{userId}'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/my_courses')
async def get_my_courses(session=Depends(validate_session_token)):
    # muestra los cursos del usuario logueado actualmente
    url_request = f'{URL_API}/student/{session[1]}'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/collaborator/{userId}')
async def get_by_collaborator(userId: UUID, _=Depends(admin_access)):
    url_request = f'{URL_API}/collaborator/{userId}'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/collaborator/my_courses')
async def get_collaborator_my_courses(session=Depends(validate_session_token)):
    # muestra los cursos donde está como colaborador el usuario logueado actualmente
    url_request = f'{URL_API}/collaborator/{session[1]}'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/hashtag/{tag}')
async def get_by_hashtag(tag: str):
    url_request = f'{URL_API}/hashtag/{tag}'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('')
async def create(newCourse: CourseCreate, session=Depends(validate_session_token)):
    url_request = URL_API
    newCourse = newCourse.copy(update={'owner': session[1]})
    query = requests.post(url_request, data=newCourse.json())
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}')
async def delete(courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.patch('/id/{courseId}')
async def update(request: CourseUpdate, courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}'
    query = requests.patch(url_request, data=request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/id/{courseId}/students')
async def get_students(courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/students'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/add_student/{userId}')
async def add_student(userId: UUID, courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/add_student/{userId}'
    query = requests.post(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/enroll')
async def enroll_student(courseId: UUID, userId: UUID = Depends(validate_subscription)):
    # Dar de alta a un curso al usuario logueado, solo si la subscripcion alcanza
    url_request = f'{URL_API}/{courseId}/add_student/{userId}'
    query = requests.post(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/remove_student/{userId}')
async def remove_student(userId: UUID, courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/remove_student/{userId}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/unsubscribe')
async def unsubscribe_student(courseId: UUID, session=Depends(validate_session_token)):
    # Dar de baja de un curso al usuario logueado
    url_request = f'{URL_API}/{courseId}/remove_student/{session[1]}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/id/{courseId}/collaborators')
async def get_collaborators(courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/collaborators'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/add_collaborator/{userId}')
async def add_collaborator(userId: UUID, courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/add_collaborator/{userId}'
    query = requests.post(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/remove_collaborator/{userId}')
async def remove_collaborator(userId: UUID, courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/remove_collaborator/{userId}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/unsubscribe_collaborator')
async def unsubscribe_collaborator(courseId: UUID, session=Depends(validate_session_token)):
    # Dar de baja de un curso como colaborador al usuario logueado
    url_request = f'{URL_API}/{courseId}/remove_collaborator/{session[1]}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/id/{courseId}/hashtags')
async def get_hashtags(courseId: UUID):
    url_request = f'{URL_API}/{courseId}/hashtags'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/add_hashtags')
async def add_hashtags(tags: List[str], courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/add_hashtags'
    query = requests.post(url_request, json=tags)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/remove_hashtags')
async def remove_hashtags(tags: List[str], courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/remove_hashtags'
    query = requests.delete(url_request, json=tags)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.put('/id/{courseId}/block')
async def set_block(block: bool = True, courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/block'
    query = requests.put(url_request, params={'block': str(block)})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.put('/id/{courseId}/status')
async def set_status(in_edition: bool, courseId: UUID = Depends(owner_access)):
    url_request = f'{URL_API}/{courseId}/status'
    query = requests.put(url_request, params={'in_edition': str(in_edition)})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())
