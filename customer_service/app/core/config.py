"""
系统配置管理
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基础配置
    APP_NAME: str = "智能电商客服与销售支持系统"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DATABASE: str = "customer_service"
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0
    
    # Milvus配置
    MILVUS_URL: str = "http://127.0.0.1:19530"
    COLLECTION_NAME: str = "customer_service"
    DIMENSION: int = 1536
    
    # JWT配置
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # AI模型配置
    OPENAI_API_KEY: Optional[str] = ""
    OPENAI_BASE_URL: Optional[str] = "https://api.deepseek.com/v1"
    MODEL_NAME: str = "deepseek-chat"

    # MEM0长期记忆框架配置
    MODEL_PROVIDER: str = "deepseek"

    EMBEDDING_PROVIDER: str = "openai"
    EMBEDDINGING_MODEL: str = "text-embedding-v4"
    EMBEDDINGING_BASE_URL: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    EMBEDDINGING_API_KEY: str = ""


    VECTOR_PROVIDER: str = "milvus"
    # MCP_SERVER服务地址
    MCP_URL: Optional[str] = "http://127.0.0.1:8000/sse"
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    
    @property
    def mysql_url(self) -> str:
        """MySQL数据库连接URL"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
    
    @property
    def redis_url(self) -> str:
        """Redis连接URL"""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 全局配置实例
settings = Settings()