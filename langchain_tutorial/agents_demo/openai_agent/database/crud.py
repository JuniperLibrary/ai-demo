from sqlalchemy.orm import Session
from . import models

def save_message(db: Session, session_id: str, message: dict):
    """保存一条消息到数据库"""
    db_message = models.ChatHistory(
        session_id=session_id,
        role=message.get("role"),
        content=message.get("content"),
        tool_calls=message.get("tool_calls"),
        tool_call_id=message.get("tool_call_id")
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_history(db: Session, session_id: str):
    """根据 session_id 获取历史记录"""
    history_orm = db.query(models.ChatHistory).filter(models.ChatHistory.session_id == session_id).order_by(models.ChatHistory.id).all()
    # 将 ORM 对象列表转换为 OpenAI 格式的字典列表
    return [item.to_dict() for item in history_orm]