import pytest
import asyncio
import sys
import time
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "gateway"))
from userService import UsersApiCalls
from DataBase import test_engine, Base

Base.metadata.drop_all(test_engine)
Base.metadata.create_all(test_engine)
UsersApiCalls.set_engine(test_engine)


def test_user_session_token_creation():
    session_token = UsersApiCalls.createSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkSessionToken(session_token)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera')
    UsersApiCalls.deleteTokenUser('id_cualquiera')


def test_user_session_token_deletion():
    session_token = UsersApiCalls.createSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkSessionToken(session_token)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera')
    UsersApiCalls.deleteTokenUser('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkSessionToken(session_token)
    assert (exists == False)
    assert (expired == True)
    assert (user_id == None)


def test_user_session_token_replaced_with_new_session():
    session_token = UsersApiCalls.createSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkSessionToken(session_token)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera')
    session_token_two = UsersApiCalls.createSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkSessionToken(session_token)
    assert (exists == False)
    assert (expired == True)
    assert (user_id == None)
    exists, expired, user_id = UsersApiCalls.checkSessionToken(session_token_two)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera')
    UsersApiCalls.deleteTokenUser('id_cualquiera')


def test_user_session_token_expirated():
    UsersApiCalls.set_session_expiration_time_in_minutes(0.05)
    session_token = UsersApiCalls.createSessionToken('id_cualquiera')
    time.sleep(4)
    exists, expired, user_id = UsersApiCalls.checkSessionToken(session_token)
    assert(exists == True)
    assert(expired == True)
    assert(user_id == None)
    UsersApiCalls.set_session_expiration_time_in_minutes(30)


def test_admin_session_token_creation():
    session_token = UsersApiCalls.createAdminSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkAdminSessionToken(session_token)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera')
    UsersApiCalls.deleteTokenUser('id_cualquiera')


def test_admin_session_token_deletion():
    session_token = UsersApiCalls.createAdminSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkAdminSessionToken(session_token)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera')
    UsersApiCalls.deleteTokenUser('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkAdminSessionToken(session_token)
    assert (exists == False)
    assert (expired == True)
    assert (user_id == None)


def test_admin_session_token_overrided():
    session_token = UsersApiCalls.createAdminSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkAdminSessionToken(session_token)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera') 
    session_token_two = UsersApiCalls.createAdminSessionToken('id_cualquiera')
    exists, expired, user_id = UsersApiCalls.checkAdminSessionToken(session_token)
    assert (exists == False)
    assert (expired == True)
    assert (user_id == None)
    exists, expired, user_id = UsersApiCalls.checkAdminSessionToken(session_token_two)
    assert (exists == True)
    assert (expired == False)
    assert (user_id == 'id_cualquiera')
    UsersApiCalls.deleteTokenUser('id_cualquiera')


def test_admin_session_token_expiration():
    UsersApiCalls.set_session_expiration_time_in_minutes(0.05)
    session_token = UsersApiCalls.createAdminSessionToken('id_cualquiera')
    time.sleep(4)
    exists, expired, user_id = UsersApiCalls.checkAdminSessionToken(session_token)
    assert(exists == True)
    assert(expired == True)
    assert(user_id == None)
    UsersApiCalls.set_session_expiration_time_in_minutes(30)

    
