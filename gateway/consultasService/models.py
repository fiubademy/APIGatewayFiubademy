from pydantic import BaseModel


class Token(BaseModel):
    token: str


class Notification(BaseModel):
    user_id: str
    message: str