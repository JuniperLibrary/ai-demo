import logging
from logging.handlers import RotatingFileHandler

# 1. 获取 Logger
logger = logging.getLogger("my_app_module")
logger.setLevel(logging.DEBUG)  # 设置全局最低级别

# 2. 创建 Handler (控制台输出)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # 控制台只看 INFO 以上

# 3. 创建 Handler (文件输出，带自动切割)
# 当文件达到 1MB 时切割，最多保留 3 个备份
file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024, backupCount=3)
file_handler.setLevel(logging.DEBUG)    # 文件记录所有细节

# 4. 创建 Formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 5. 将 Formatter 绑定到 Handler
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 6. 将 Handler 绑定到 Logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 使用
logger.info("这条日志会出现在控制台和文件中")
logger.debug("这条日志只会出现在文件中")