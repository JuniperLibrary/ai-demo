from pydantic import BaseModel

class ChatReq(BaseModel):
    user_message: str
