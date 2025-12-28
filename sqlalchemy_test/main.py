from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import os
import dotenv

dotenv.load_dotenv()


# --- 1. 配置 SQLAlchemy ---
DATABASE_URL = os.getenv('DATABASE_URL')

# 创建引擎
engine = create_engine(DATABASE_URL)
# 创建基类
Base = declarative_base()
# 创建 Session 工厂
SessionLocal = sessionmaker(bind=engine)

# --- 2. 定义模型 (Model) ---
# 这就是 SQLAlchemy 的核心：用类来代表表
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(255), index=True)
    role = Column(String(50), nullable=False)
    content = Column(Text, nullable=True)
    # SQLAlchemy 对 Postgres JSONB 的原生支持
    tool_calls = Column(JSONB, nullable=True)
    tool_call_id = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.now)

# 自动建表 (如果表不存在)
Base.metadata.create_all(bind=engine)

# --- 3. 替换原有的 save_message ---
def save_message_orm(session_id, message):
    db = SessionLocal()
    try:
        # 直接实例化对象，不用写 SQL INSERT 语句
        new_msg = ChatHistory(
            session_id=session_id,
            role=message.get("role"),
            content=message.get("content"),
            tool_calls=message.get("tool_calls"), # ORM 会自动处理 JSON 序列化
            tool_call_id=message.get("tool_call_id")
        )
        db.add(new_msg)
        db.commit()
    finally:
        db.close()