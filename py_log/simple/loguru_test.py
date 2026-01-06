# pip install loguru
from loguru import logger

# 自动带颜色、时间、层级
logger.debug("调试")
logger.info("信息")

# 一行代码配置写文件（带切割、压缩、保留时间）
logger.add("file_{time}.log", rotation="500 MB", retention="10 days", compression="zip")