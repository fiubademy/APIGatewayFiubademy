import requests
from uuid import UUID
from fastapi import HTTPException, status, Depends
from gateway.userService.UsersApiCalls import checkAdminSessionToken, checkSessionToken, setSubscription
from gateway.userService.UsersApiCalls import URL_API_USUARIOS as URL_API_USERS
from courseService.setupCourseApi import URL_API


def validate_session_token(sessionToken: UUID):
    # devuelve una tupla (is_admin, userId) si es un token de sesion válido. Si no, lanza una excepción
    _, _, userId = checkSessionToken(str(sessionToken))
    if not userId:
        _, _, userId = checkAdminSessionToken(str(sessionToken))
        if not userId:
            raise HTTPException(
                status_code=498, detail="Invalid session token.")
        return True, userId
    return False, userId


def is_owner(userId, courseId):
    url_request = f'{URL_API}/{courseId}/owner'
    query = requests.get(url_request)
    if query.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Failed to reach backend.')
    return {'ownerId': userId} == query.json()


def is_collaborator(userId, courseId):
    url_request = f'{URL_API}/{courseId}/collaborators'
    query = requests.get(url_request)
    if query.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Failed to reach backend.')
    return userId in query.json()


def is_student(userId, courseId):
    url_request = f'{URL_API}/{courseId}/students'
    query = requests.get(url_request)
    if query.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            detail='Failed to reach backend.')
    return userId in query.json()


def get_user_sub_level(userId):
    # Api de usuarios para gettear el sub level
    url_request = f'{URL_API_USERS}/ID/{userId}'
    query = requests.get(url_request)
    if query.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=query.status_code,
                            detail='Failed to reach backend.')
    return query.json()['sub_level']


def get_course_sub_level(courseId):
    url_request = f'{URL_API}/all/1'
    query = requests.get(url_request, params={'courseId': courseId})
    if query.status_code != status.HTTP_200_OK:
        raise HTTPException(status_code=query.status_code,
                            detail='Failed to reach backend.')
    return query.json()['content'][0]['sub_level']


def admin_access(session=Depends(validate_session_token)):
    if not session[0]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized operation.")


def owner_access(courseId: UUID, session=Depends(validate_session_token)):
    if session[0] or is_owner(session[1], courseId):
        return courseId
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized operation.")


def teacher_access(courseId: UUID, session=Depends(validate_session_token)):
    if session[0] or is_owner(session[1], courseId) or is_collaborator(session[1], courseId):
        return courseId
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized operation.")


def student_access(courseId: UUID, session=Depends(validate_session_token)):
    if session[0] or is_student(session[1], courseId) or is_owner(session[1], courseId):
        return courseId
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized operation.")


def new_collaborator_access(courseId: UUID, session=Depends(validate_session_token)):
    if is_owner(session[1], courseId) or is_collaborator(session[1], courseId) or is_student(session[1], courseId):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is already in course.')
    return session[1]


def new_student_access(courseId: UUID, session=Depends(validate_session_token)):
    if is_owner(session[1], courseId) or is_collaborator(session[1], courseId) or is_student(session[1], courseId):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User is already in course.')
    elif get_user_sub_level(session[1]) >= get_course_sub_level(courseId):
        return session[1]
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Subscription level unsatisfied.")
