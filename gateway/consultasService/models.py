from pydantic import BaseModel


class Token(BaseModel):
    fcm_token: str


class Notification(BaseModel):
    user_id: str
    message: str