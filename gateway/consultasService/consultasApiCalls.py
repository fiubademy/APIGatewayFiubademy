from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse
from fastapi import Depends, APIRouter, status
import requests

from consultasService.models import Token, Notification
from courseService.validations import validate_session_token
from consultasService.setupConsultasApi import URL_API

router = APIRouter(dependencies=[Depends(validate_session_token)])


@ router.put('/update_fcm_token')
async def update_fcm_token(token: Token, session=Depends(validate_session_token)):
    '''
    Actualiza el token de FCM asociado al usuario.
    '''
    url_request = f'{URL_API}/update_token'
    token = token.copy(update={'user_id': session[1]})
    query = requests.put(url_request, data=token.json(), headers={"Content-type":"application/json"})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())


@ router.post('/notify_user')
async def notify_user(notification: Notification):
    '''
    Envía una notificación a otro usuario con un mensaje.
    '''
    url_request = f'{URL_API}/notify_user'
    query = requests.post(url_request, data=notification.json(), headers={"Content-type":"application/json"})
    if query.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Failed to reach backend.')
    return JSONResponse(status_code=query.status_code, content=query.json())



