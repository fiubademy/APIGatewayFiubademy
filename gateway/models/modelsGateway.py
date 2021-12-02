from typing import Optional
from pydantic import EmailStr
from pydantic.main import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from DataBase import Base


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

class RegisteredUserHistory(Base):
    __tablename__ = "registered_users_history"
    user_id = Column(String(500), primary_key = True, nullable = False, unique = True)
    date_created = Column(DateTime, nullable = False)
    is_federated = Column(String, nullable = False)

    def __str__(self):
        return (self.user_id, self.date_created)


class LoginHistory(Base):
    __tablename__ = "login_history"
    user_id = Column(String(500), nullable = False, primary_key = True)
    date_logged = Column(DateTime, primary_key = True, nullable = False)
    is_federated = Column(String, nullable = False)

    def __str__(self):
        return (self.user_id, self.date_logged)


class RecoverPasswordHistory(Base):
    __tablename__ = "recover_password_history"
    user_id = Column(String(500), nullable = False, primary_key = True)
    date_recovered = Column(DateTime, primary_key = True, nullable = False)

    def __str__(self):
        return (self.user_id, self.date_recovered)


class BlockHistory(Base):
    __tablename__ = "block_history"
    user_id = Column(String(500), nullable = False, primary_key = True)
    date_blocked = Column(DateTime, primary_key = True, nullable = False)

    def __str__(self):
        return (self.user_id, self.date_blocked)