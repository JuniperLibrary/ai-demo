from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import dotenv
dotenv.load_dotenv()

from core.shared.config import get_logger

logger = get_logger("agent.openai_agent", log_file="logs/openai_agent.log", format_style="standard")

# 创建数据库引擎
engine = create_engine(os.getenv("DATABASE_URL"))

# 创建一个 Session 工厂，后续可以用它来创建独立的数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 这个函数可以用来确保表被创建
def init_db():
    from .models import Base
    logger.info(f"正在初始化数据库，创建所有表...")
    Base.metadata.create_all(bind=engine)
    logger.info(f"数据库初始化完成。")