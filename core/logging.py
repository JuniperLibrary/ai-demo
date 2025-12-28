import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler



def setup_logging():
    """配置日志系统"""

    # 抑制 passlib.handlers.bcrypt 的版本读取警告
    # warnings.filterwarnings("ignore", message=".*error reading bcrypt version.*", category=UserWarning, module="passlib.handlers.bcrypt")
    # 也抑制相关的 passlib 日志记录器的警告
    # logging.getLogger("passlib.handlers.bcrypt").setLevel(logging.ERROR)

    # 配置日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel("INFO")

    # 清除已有的 handlers（避免重复添加）
    logger.handlers.clear()

    # 添加控制台输出
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 如果不是调试模式，添加文件日志
    if not False:
        try:
            os.makedirs("logs", exist_ok=True)
            # 使用 TimedRotatingFileHandler 替代 RotatingFileHandler
            # 在 Windows 多进程环境下更稳定
            file_handler = TimedRotatingFileHandler(
                "logs/app.log",
                when='midnight',  # 每天午夜轮转
                interval=1,
                backupCount=30,  # 保留30天
                encoding="utf-8",
                delay=False,
                utc=False
            )
            file_handler.suffix = "%Y-%m-%d"  # 备份文件后缀格式
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            # 如果文件日志配置失败，至少保证控制台输出可用
            logger.warning(f"无法配置文件日志: {e}，将只使用控制台输出")

    return logger