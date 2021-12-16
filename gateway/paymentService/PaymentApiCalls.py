import requests
import uuid
from uuid import UUID
from fastapi import status, Depends
from typing import List, Optional
from starlette.responses import JSONResponse
from sqlalchemy.sql import null
from sqlalchemy.orm import sessionmaker
from fastapi import APIRouter, Body
from datetime import datetime, timedelta
import sys
import os
from fastapi.exceptions import HTTPException

from gateway.courseService.validations import admin_access

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from courseService.validations import validate_session_token

URL_API_PAY = 'https://api-smartcontracts-fiubademy.herokuapp.com'

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


@router.get('/wallet/{sessionToken}')
async def get_wallet_user(session = Depends(validate_session_token)):
    query = requests.get(URL_API_PAY+'/wallet/'+session[1])
    if not query.json():
        return JSONResponse(status_code = status.HTTP_404_NOT_FOUND, content="User has no wallet created yet.")
    return JSONResponse(status_code = query.status_code, content = query.json())


@router.get('/wallet')
async def get_wallets(session = Depends(admin_access)):
    query = requests.get(URL_API_PAY+'/wallet')
    return JSONResponse(status_code = query.status_code, content = query.json())


@router.post('/wallet')
async def create_wallet_for_user(session = Depends(validate_session_token)):
    user_id = session[1]
    print('{"user_id" : "'+user_id+'" }')
    query = requests.post(
        URL_API_PAY+'/wallet',
        data = '{"user_id":"'+user_id+'"}',
        headers = {"Content-Type": "application/json"}    
    )
    return JSONResponse(status_code = query.status_code, content = query.json())


@router.post('/deposit')
async def deposit_to_contract(amount_ether: float = Body(embed = True, default = None), session = Depends(validate_session_token)):
    user_id = session[1]
    query = requests.post(
        URL_API_PAY+'/deposit',
        data = '{"senderId" : "'+user_id+'", "amountInEthers":'+ str(amount_ether) +'}',
        headers = {"Content-Type": "application/json"} 
    )
    return JSONResponse(status_code = query.status_code, content = query.json())


@router.post('/deposit_owner')
async def deposit_to_contract_owner(amount_ether: float = Body(embed = True, default = None), session = Depends(admin_access)):
    query = requests.post(
        URL_API_PAY+'/deposit_owner',
        data = '{"amountInEthers":'+ str(amount_ether) +'}',
        headers = {"Content-Type": "application/json"} 
    )
    return JSONResponse(status_code = query.status_code, content = query.json())


@router.get('/deposit/{txHash}')
async def get_deposit(txHash:str, session = Depends(admin_access)):
    query = requests.get(URL_API_PAY+'/deposit/'+txHash)
    return JSONResponse(status_code = query.status_code, content = query.json())
