import logging

# 配置日志（只需配置一次）
logging.basicConfig(
    level=logging.INFO, # 设置级别
    format='%(asctime)s - %(levelname)s - %(message)s', # 设置格式
    filename='app.log', # 输出到文件（不写则输出到控制台）
    filemode='a' # 追加模式
)

logging.debug("这是一条调试信息") # 不会显示，因为级别是 INFO
logging.info("程序启动")
logging.warning("磁盘空间不足")
logging.error("数据库连接失败")