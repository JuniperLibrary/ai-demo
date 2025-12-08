# pip list | grep langchain

pip list | grep langchain                                                                                                                             
langchain                                0.3.0
langchain-chroma                         0.1.4
langchain-community                      0.3.0
langchain-core                           0.3.0
langchain-openai                         0.2.0
langchain-text-splitters                 0.3.0

# pip uninstall -y langchain langchain-core langchain-community langchain-openai langchain-chroma langchain-classic langchain-text-splitters

# 强制覆盖安装，指定官方版本号
# pip install --force-reinstall --no-cache-dir langchain==0.3.0 langchain-core==0.3.0 langchain-community==0.3.0 langchain-openai==0.2.0 langchain-chroma==0.1.4