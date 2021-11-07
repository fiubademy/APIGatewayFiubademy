from typing import Optional
from pydantic import EmailStr
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from gateway.DataBase import Base


class SessionToken(Base):
    __tablename__ = "session_tokens"
    session_token = Column(String(500), primary_key = True, nullable=False)
    user_id = Column(String(500), nullable=False, unique=True)
    time_last_action = Column(DateTime, nullable=False)

    def __str__(self):
        return self.session_token


class AdminSessionToken(Base):
    __tablename__ = "admin_session_tokens"
    session_token = Column(String(500), primary_key = True, nullable=False)
    user_id = Column(String(500), nullable=False, unique=True)
    time_last_action = Column(DateTime, nullable=False)

    def __str__(self):
        return self.session_token
