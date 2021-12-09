from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from typing import List, Optional
from fastapi import Depends, APIRouter, status
from uuid import UUID
import requests

from courseService.models import CourseCreate, CourseUpdate, CourseFilter, ReviewCreate, ContentCreate
from courseService.validations import admin_access, validate_session_token, owner_access, student_access, teacher_access, validate_new_collaborator, validate_new_student, user_by_email
from courseService.setupCourseApi import URL_API

router = APIRouter(dependencies=[Depends(validate_session_token)])


@router.get('/all/{page_num}')
async def get_courses(page_num: int, filter: CourseFilter = Depends()):
    '''
    Muestra todos los cursos que cumplan los filtros. Se muestran usando paginación.
    '''
    url_request = f'{URL_API}/all/{page_num}'
    query = requests.get(url_request, params=filter.__dict__)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/student/{userId}/{pagenum}')
async def get_by_student(pagenum: int, userId: UUID, _=Depends(admin_access)):
    '''
    Muestra los cursos del usuario especificado.
    Permisos necesarios: admin.
    '''
    url_request = f'{URL_API}/all/{pagenum}'
    query = requests.get(url_request, params={'student': userId})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/my_courses/{pagenum}')
async def get_my_courses(pagenum: int, courseId: Optional[UUID] = None, session=Depends(validate_session_token)):
    '''
    Muestra los cursos del usuario logueado actualmente.
    '''
    url_request = f'{URL_API}/all/{pagenum}'
    query = requests.get(url_request, params={
                         'student': session[1], 'id': courseId})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/collaborator/{userId}/{pagenum}')
async def get_by_collaborator(pagenum: int, userId: UUID, _=Depends(admin_access)):
    '''
    Muestra todos los cursos en los que el usuario especificado está inscripto como colaborador.
    Permisos necesarios: admin.
    '''
    url_request = f'{URL_API}/all/{pagenum}'
    query = requests.get(url_request, params={'collaborator': userId})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/my_courses/collaborator/{pagenum}')
async def get_collaborator_my_courses(pagenum: int, courseIdFilter: Optional[UUID] = None, session=Depends(validate_session_token)):
    '''
    Muestra los cursos donde está como colaborador el usuario logueado actualmente.
    '''
    url_request = f'{URL_API}/all/{pagenum}'
    query = requests.get(url_request, params={'collaborator': session[1], 'id': courseIdFilter})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/my_courses/owner/{pagenum}')
async def get_my_courses_owned(pagenum: int, session=Depends(validate_session_token)):
    '''  
    Muestra los cursos donde está como colaborador el usuario logueado actualmente.
    '''
    url_request = f'{URL_API}/all/{pagenum}'
    query = requests.get(url_request, params={'owner': session[1]})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/id/{courseId}/students')
async def get_students(courseId: UUID = Depends(owner_access)):
    '''
    Muestra la lista de los estudiantes inscriptos al curso. 
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/students'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/id/{courseId}/collaborators')
async def get_collaborators(courseId: UUID = Depends(owner_access)):
    '''
    Muestra la lista de colaboradores del curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/collaborators'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/id/{courseId}/reviews')
async def get_reviews(self: bool, courseId: UUID, pagenum: Optional[int] = 1, session=Depends(validate_session_token)):
    '''
    Si el parámetro self es true devuelve la review cargada por el usuario en el curso especificado.
    Si no, devuelve todas las reviews de dicho curso, usando paginación.

    Permisos necesarios: solo tener un token sesión válido, es información pública.
    '''
    if self:
        url_request = f'{URL_API}/{courseId}/review/{session[1]}'
    else:
        url_request = f'{URL_API}/{courseId}/all_reviews/{pagenum}'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.get('/id/{courseId}/get_content_list')
async def get_content_list(courseId: UUID = Depends(student_access)):
    '''
    Devuelve la lista de contenidos del curso.
    Permisos necesarios: estar inscripto al curso, o bien ser el dueño o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/get_content_list'
    query = requests.get(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.patch('/id/{courseId}')
async def update(request: CourseUpdate, courseId: UUID = Depends(owner_access)):
    '''
    Actualiza los campos especificados que sean no nulos.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}'
    query = requests.patch(url_request, data=request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('')
async def create(newCourse: CourseCreate, session=Depends(validate_session_token)):
    '''
    Permisos necesarios: cualquier usuario válido puede crear un curso.
    '''
    url_request = URL_API
    newCourse = newCourse.copy(update={'owner': session[1]})
    query = requests.post(url_request, data=newCourse.json())
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/add_student/{userId}')
async def add_student(userId: UUID, courseId: UUID = Depends(owner_access)):
    '''
    Agrega un usuario a un curso. 
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    validate_new_student(courseId, userId)
    url_request = f'{URL_API}/{courseId}/add_student/{userId}'
    query = requests.post(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/add_collaborator/{userId}')
async def add_collaborator(userId: UUID = Depends(user_by_email), courseId: UUID = Depends(owner_access)):
    '''
    Agrega al usuario como colaborador del curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    validate_new_collaborator(courseId, userId)
    url_request = f'{URL_API}/{courseId}/add_collaborator/{userId}'
    query = requests.post(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/enroll')
async def enroll_student(courseId: UUID, session=Depends(validate_session_token)):
    '''
    Da de alta a un curso al usuario logueado actualemnte.
    Permisos necesario: tener nivel de subscripción suficiente, según el curso.
    '''
    validate_new_student(courseId, session[1])
    url_request = f'{URL_API}/{courseId}/add_student/{session[1]}'
    query = requests.post(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/add_hashtags')
async def add_hashtags(tags: List[str], courseId: UUID = Depends(owner_access)):
    '''
    Agrega los hashtags a un curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/add_hashtags'
    hashtags = {'tags': tags}
    query = requests.post(url_request, json=hashtags)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/id/{courseId}/add_content')
async def add_content(new: ContentCreate, courseId: UUID = Depends(owner_access)):
    '''
    Agregar un contenido (nombre y link a un video) a un curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/add_content'
    query = requests.post(url_request, data=new.json())
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}', summary='Delete course')
async def delete(courseId: UUID = Depends(owner_access)):
    '''
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/remove_student/{userId}')
async def remove_student(userId: UUID, courseId: UUID = Depends(owner_access)):
    '''
    Da de baja un usuario de un curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/remove_student/{userId}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/remove_collaborator/{userId}')
async def remove_collaborator(userId: UUID, courseId: UUID = Depends(owner_access)):
    '''
    Elimina al usuario de los colaboradores del curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/remove_collaborator/{userId}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/unsubscribe')
async def unsubscribe_student(courseId: UUID, session=Depends(validate_session_token)):
    '''
    Da de baja de un curso al usuario logueado.
    '''
    url_request = f'{URL_API}/{courseId}/remove_student/{session[1]}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/unsubscribe_collaborator')
async def unsubscribe_collaborator(courseId: UUID, session=Depends(validate_session_token)):
    '''
    Elimina al usuario logueado actualmente de los colaboradores del curso.
    '''
    url_request = f'{URL_API}/{courseId}/remove_collaborator/{session[1]}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('/id/{courseId}/remove_hashtags')
async def remove_hashtags(tags: List[str], courseId: UUID = Depends(owner_access)):
    '''
    Elimina los hashtags del curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/remove_hashtags'
    hashtags = {'tags': tags}
    query = requests.delete(url_request, json=hashtags)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.delete('id/{courseId}/remove_content/{contentId}')
async def remove_content(contentId: str, _=Depends(owner_access)):
    '''
    Elimina de un curso un contenido según si id (obtenido desde get_content_list).
    Permisos necesarios: ser dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/remove_content/{contentId}'
    query = requests.delete(url_request)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.put('/id/{courseId}/block')
async def set_block(block: bool = True, courseId: UUID = Depends(owner_access)):
    '''
    Bloquea el curso.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/block'
    query = requests.put(url_request, params={'block': str(block)})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.put('/id/{courseId}/status')
async def set_status(in_edition: bool, courseId: UUID = Depends(owner_access)):
    '''
    Modifica el estado del curso en edición.
    Permisos necesarios: ser el dueño del curso o un admin.
    '''
    url_request = f'{URL_API}/{courseId}/status'
    query = requests.put(url_request, params={'in_edition': str(in_edition)})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.put('/id/{courseId}/add_review')
async def add_review(courseId: UUID, new: ReviewCreate, session=Depends(validate_session_token)):
    '''
    Agrega una nueva review al curso especificado, asociada al id del usuario logueado.    
    Permisos necesarios: solo tener un token sesión válido, es una operación pública.
    '''
    url_request = f'{URL_API}/{courseId}/review'
    new = new.dict()
    new.update({'user_id': session[1]})
    query = requests.put(url_request, json=new)
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())
