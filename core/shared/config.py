#!/usr/bin/env python3
"""
统一日志配置系统 - 支持多种格式和输出方式
"""

import logging
import sys
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """带颜色的控制台日志格式化器"""
    
    # ANSI颜色代码
    COLORS = {
        'DEBUG': '\033[36m',    # 青色
        'INFO': '\033[32m',     # 绿色
        'WARNING': '\033[33m',  # 黄色
        'ERROR': '\033[31m',    # 红色
        'CRITICAL': '\033[35m', # 紫色
        'RESET': '\033[0m'      # 重置
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        reset_color = self.COLORS['RESET']
        
        # 添加颜色
        record.levelname = f"{log_color}{record.levelname}{reset_color}"
        
        return super().format(record)


class JSONFormatter(logging.Formatter):
    """JSON格式日志格式化器"""
    
    def format(self, record):
        import json
        
        log_entry = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # 添加额外字段
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = record.user_id
        if hasattr(record, 'conversation_id'):
            log_entry['conversation_id'] = record.conversation_id
        if hasattr(record, 'agent_type'):
            log_entry['agent_type'] = record.agent_type
            
        return json.dumps(log_entry, ensure_ascii=False)


def get_logger(
    name: str, 
    level: Optional[str] = None,
    log_file: Optional[str] = None,
    enable_console: bool = True,
    format_style: str = 'standard',  # 'standard', 'json', 'simple'
    **kwargs
) -> logging.Logger:
    """
    获取统一配置的日志记录器
    
    Args:
        name: 日志器名称
        level: 日志级别，默认使用全局设置
        log_file: 日志文件路径，如果不指定则不写文件
        enable_console: 是否启用控制台输出
        format_style: 格式样式 - standard/json/simple
        **kwargs: 额外的日志配置参数
    
    Returns:
        logging.Logger: 配置好的日志记录器
    """
    
    logger = logging.getLogger(name)
    
    # 避免重复添加handler
    if logger.handlers:
        return logger
        
    # 设置日志级别
    if level is None:
        level = "INFO"
    logger.setLevel(getattr(logging, level.upper()))
    
    # 选择格式化器
    if format_style == 'json':
        formatter = JSONFormatter()
    elif format_style == 'simple':
        formatter = logging.Formatter("%(levelname)s: %(message)s")
    else:  # standard
        if enable_console and sys.stdout.isatty():  # 终端环境使用彩色
            formatter = ColoredFormatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
        else:
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
    
    # 控制台输出
    if enable_console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # 文件输出
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # 使用按日期轮转的文件处理器
        file_handler = TimedRotatingFileHandler(
            log_file,
            when='midnight',
            interval=1,
            backupCount=30,  # 保留30天
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_agent_logger(agent_type: str, logger_name: Optional[str] = None) -> logging.Logger:
    """
    获取Agent专用日志记录器
    
    Args:
        agent_type: Agent类型
        logger_name: 自定义日志器名称
    
    Returns:
        logging.Logger: Agent专用日志记录器
    """
    if logger_name is None:
        logger_name = f"agent.{agent_type}"
    
    log_file = None
    if not False:  # 生产环境写文件
        log_file = f"logs/agents/{agent_type}.log"
    
    return get_logger(
        name=logger_name,
        log_file=log_file,
        format_style='standard'
    )


def get_conversation_logger(conversation_id: str, agent_type: str) -> logging.Logger:
    """
    获取对话专用日志记录器
    
    Args:
        conversation_id: 对话ID
        agent_type: Agent类型
    
    Returns:
        logging.Logger: 对话专用日志记录器
    """
    logger_name = f"agent.{agent_type}.conversation.{conversation_id[:8]}"
    
    log_file = None
    if not False:
        log_file = f"logs/conversations/{agent_type}/{conversation_id[:8]}.log"
    
    return get_logger(
        name=logger_name,
        log_file=log_file,
        format_style='standard'
    )


def get_state_logger(state_name: str, agent_type: str) -> logging.Logger:
    """
    获取状态专用日志记录器
    
    Args:
        state_name: 状态名称
        agent_type: Agent类型
    
    Returns:
        logging.Logger: 状态专用日志记录器
    """
    logger_name = f"agent.{agent_type}.state.{state_name}"
    return get_agent_logger(agent_type, logger_name)


def setup_root_logger():
    """
    设置根日志记录器 - 兼容原有的setup_logging函数
    """
    import warnings
    
    # 抑制 passlib 警告
    warnings.filterwarnings("ignore", message=".*error reading bcrypt version.*", 
                          category=UserWarning, module="passlib.handlers.bcrypt")
    
    # 设置SQLAlchemy日志级别为WARNING，避免SQL语句打印
    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    sqlalchemy_logger.setLevel(logging.WARNING)
    
    # 设置根日志记录器
    # 即使在DEBUG模式下也写入日志文件，方便调试
    log_file = "logs/app.log"
    # 如果设置了LOG_FILE环境变量，优先使用环境变量的值
    # custom_log_file = os.environ.get('BOODSEEK_LOG_FILE')
    # if custom_log_file:
    #     log_file = custom_log_file
    #
    root_logger = get_logger(
        name="root",
        level="INFO",
        log_file=log_file,  # 始终写入日志文件（如果配置了）
        enable_console=True,
        format_style='standard'
    )
    
    return root_logger


# 为了向后兼容
setup_logging = setup_root_logger

# 提供默认的日志记录器
console_logger = get_logger("console", enable_console=True, log_file="logs/app.log")
file_logger = get_logger("file", enable_console=False, log_file="logs/app.log")
# 禁用向上传播，避免重复日志
console_logger.propagate = False