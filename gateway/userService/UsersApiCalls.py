from fastapi import status
from typing import List, Optional
from pydantic import EmailStr
from starlette.responses import JSONResponse
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.sql import null
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from fastapi import APIRouter
from datetime import datetime, timedelta
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from gateway.models.modelsGateway import SessionToken, AdminSessionToken
import uuid
import hashlib
import requests

URL_API = 'https://api-usuarios-fiubademy.herokuapp.com/users'
SESSION_EXPIRATION_TIME_IN_MINUTES = 30

router = APIRouter()
Session = None
session = None
engine = None


def set_engine(engine_rcvd):
    global engine
    global Session
    global session
    engine = engine_rcvd
    Session = sessionmaker(bind=engine)
    session = Session()


def checkSessionToken(sessionToken):
    try:
        ses_token_reg = session.query(SessionToken).filter(SessionToken.session_token == sessionToken).first()
    except NoResultFound as e:
        return False, True, None #Not Exists, Expired, ID = None
    if not ses_token_reg:
        return False, True, None #Not Exists, Expired, ID = None
    time_delta = (datetime.now() - ses_token_reg.time_last_action)
    total_seconds = time_delta.total_seconds()
    minutes_since_no_action = total_seconds/60
    if minutes_since_no_action > SESSION_EXPIRATION_TIME_IN_MINUTES:
        return True, True, None #Exists, Expired, ID = None
    ses_token_reg.time_last_action = datetime.now()
    session.add(ses_token_reg)
    session.commit()
    return True, False, ses_token_reg.user_id #Token Exists, Token Not Expired, and ID not Null


def checkAdminSessionToken(sessionToken):
    try:
        ses_token_reg = session.query(AdminSessionToken).filter(AdminSessionToken.session_token == sessionToken).first()
    except NoResultFound as e:
        return False, True, None #Not Exists, Expired, ID = None
    if not ses_token_reg:
        return False, True, None #Not Exists, Expired, ID = None
    time_delta = (datetime.now() - ses_token_reg.time_last_action)
    total_seconds = time_delta.total_seconds()
    minutes_since_no_action = total_seconds/60
    if minutes_since_no_action > SESSION_EXPIRATION_TIME_IN_MINUTES:
        session.query(AdminSessionToken).filter(AdminSessionToken.session_token == sessionToken).delete()
        return True, True, None #Exists, Expired, ID = None
    ses_token_reg.time_last_action = datetime.now()
    session.add(ses_token_reg)
    session.commit()
    return True, False, ses_token_reg.user_id #Token Exists, Token Not Expired, and ID not Null


def createAdminSessionToken(user_id):
    session.query(AdminSessionToken).filter(AdminSessionToken.user_id == user_id).delete()
    sessionToken = str(uuid.uuid4())
    session.add(AdminSessionToken(session_token=sessionToken, user_id = user_id, time_last_action = datetime.now()))
    session.commit()
    return sessionToken


def createSessionToken(user_id):
    session.query(SessionToken).filter(SessionToken.user_id == user_id).delete()
    sessionToken = str(uuid.uuid4())
    session.add(SessionToken(session_token=sessionToken, user_id = user_id, time_last_action = datetime.now()))
    session.commit()
    return sessionToken


def deleteTokenUser(user_id):
    session.query(SessionToken).filter(SessionToken.user_id == user_id).delete()
    session.query(AdminSessionToken).filter(AdminSessionToken.user_id == user_id).delete()
    session.commit()


@router.get('/{page_num}')
async def getUsers(page_num: int, emailFilter: Optional[str] = '', usernameFilter: Optional[str] = ''):
    url_request = URL_API + '/' + str(page_num)
    query_params_quantity = 0
    if emailFilter != '' or usernameFilter != '':
        url_request = url_request + '?'
        if emailFilter != '':
            query_params_quantity += 1
            url_request = url_request + 'emailFilter=' + emailFilter
        if usernameFilter != '':
            if query_params_quantity > 0:
                url_request = url_request + '&'
            url_request = url_request + 'usernameFilter=' + usernameFilter
    query = requests.get(url_request)
    return JSONResponse(status_code = query.status_code, content=query.json())


@router.get('/ID/{user_id}', status_code=status.HTTP_200_OK)
async def getUser(user_id= ''):
    url_request = URL_API + '/ID/' + user_id
    query = requests.get(url_request).json()
    return JSONResponse(status_code = query.status_code, content=query.json())


@router.post('/get_token', status_code=status.HTTP_200_OK)
async def getTokenForRecPasswd(email:str):
    url_request = URL_API + '/get_token'
    query = requests.post(url_request, params= {'email':email} )
    return JSONResponse(status_code = query.status_code, content = query.json())


@router.post('/login')
async def loginUser(email:str, password:str):
    url_request_user = URL_API + '/1?' + 'emailFilter=' + email
    query_user = requests.get(url_request_user)
    if query_user.status_code == status.HTTP_200_OK:
        if query_user.json()['content'][0]['is_blocked'] == 'Y':
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content = "User " + email + " is currently blocked and can not be logged in.")
    url_request = URL_API + '/login'
    retorno = requests.post(url_request, params={'email':email, 'password': password})
    if retorno.status_code == status.HTTP_202_ACCEPTED:
        return JSONResponse(status_code=status.HTTP_200_OK, content=createSessionToken(retorno.json()))
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED, content=retorno.json())


@router.post('/', status_code=status.HTTP_201_CREATED)
async def createUser(username: str, email: EmailStr, password: str):
    url_request = URL_API + '/'
    retorno = requests.post(url_request, params={'username':username, 'email':email, 'password':password})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.post('/createAdmin', status_code=status.HTTP_201_CREATED)
async def createAdmin(username: str, email: EmailStr, password: str):
    url_request = URL_API + '/createAdmin'
    retorno = requests.post(url_request, params={'username':username, 'email':email, 'password':password})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())
  
   
@router.delete('/{session_token}', status_code=status.HTTP_202_ACCEPTED)
async def deleteUser(session_token: str):
    tokenExists, tokenExpired, user_id = checkSessionToken(session_token)
    if not tokenExists:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token does not exist')
    if tokenExpired:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token expired.')
    url_request = URL_API + '/' + user_id
    retorno = requests.delete(url_request)
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.patch('/{session_token}')
async def patchUser(session_token: str, email: Optional[str] = None, username: Optional[str] = None):
    tokenExists, tokenExpired, user_id = checkSessionToken(session_token)
    if not tokenExists:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token does not exist')
    if tokenExpired:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token expired.')
    url_request = URL_API + '/' + user_id
    retorno = requests.patch(url_request, params={'email':email, 'username': username})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.patch('/changePassword/{session_token}')
async def changePassword(session_token: str, oldPassword: str, newPassword: str):
    tokenExists, tokenExpired, user_id = checkSessionToken(session_token)
    if not tokenExists:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token does not exist')
    if tokenExpired:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token expired.')
    url_request = URL_API + '/changePassword/' + user_id
    retorno = requests.patch(url_request, params={'oldPassword':oldPassword, 'newPassword': newPassword})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.patch('/recoverPassword/{token}')
async def recoverPassword(newPassword: str, token:str):
    url_request = URL_API + '/recoverPassword/' + token
    retorno = requests.patch(url_request, params={'newPassword': newPassword, 'token': token})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.patch('/{session_token}/set_sub')
async def setSubscription(session_token: str, sub_level: int):
    tokenExists, tokenExpired, user_id = checkSessionToken(session_token)
    if not tokenExists:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token does not exist')
    if tokenExpired:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token expired.')
    url_request = URL_API + '/' + user_id + '/set_sub'
    retorno = requests.patch(url_request, params={'user_id': user_id, 'sub_level': sub_level})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.patch('/{session_token}/set_location')
async def setLocation(session_token: str, latitude: float, longitude: float):
    tokenExists, tokenExpired, user_id = checkSessionToken(session_token)
    if not tokenExists:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token does not exist')
    if tokenExpired:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Session Token expired.')
    url_request = URL_API + '/' + user_id + '/set_location'
    retorno = requests.patch(url_request, params={'user_id': user_id, 'latitude': latitude, 'longitude': longitude})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.patch('/{user_id}/toggleBlock')
async def toggleBlockUser(user_id: str, admin_ses_token: str):
    tokenExists, tokenExpired, user_id_admin = checkAdminSessionToken(admin_ses_token)
    if not tokenExists:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Admin Session Token does not exist')
    if tokenExpired:
        return JSONResponse(status_code = status.HTTP_403_FORBIDDEN, content='Admin Session Token expired.')
    deleteTokenUser(user_id)
    url_request = URL_API + '/' + user_id + '/toggleBlock'
    retorno = requests.patch(url_request, params={'user_id': user_id})
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())


@router.post('/loginAdmin')
async def loginAdmin(email:str, password:str):
    url_request = URL_API + '/loginAdmin'
    retorno = requests.post(url_request, params={'email':email, 'password': password})
    if retorno.status_code == status.HTTP_202_ACCEPTED:
        return JSONResponse(status_code = retorno.status_code, content = createAdminSessionToken(retorno.json()))
    return JSONResponse(status_code = retorno.status_code, content = retorno.json())