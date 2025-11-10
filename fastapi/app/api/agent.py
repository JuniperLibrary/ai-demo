from fastapi import APIRouter
from schemas.agent_req import ChatReq
from service.agent_service import chat_agent

router = APIRouter()

@router.post("/chat")
async def chat(req: ChatReq):
    return {"answer": await chat_agent(req.user_message)}
