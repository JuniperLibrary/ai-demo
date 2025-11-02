import os
import dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate

# 加载环境变量
dotenv.load_dotenv()

# 设置OpenAI环境变量
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_BASE_URL'] = os.getenv("OPENAI_BASE_URL")

class PostgresSQLTool:
    """
    PostgreSQL数据库SQL查询生成工具
    基于LangChain和大语言模型，帮助用户自动生成和执行SQL查询
    """
    
    def __init__(self, user, password, host, port, database):
        """
        初始化PostgreSQL连接
        
        参数:
            user: 数据库用户名
            password: 数据库密码
            host: 数据库主机地址
            port: 数据库端口号
            database: 数据库名称
        """
        # PostgreSQL连接URI
        # postgresql+psycopg2://用户名:密码@主机:端口/数据库名
        self.db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        self.db = SQLDatabase.from_uri(self.db_uri)
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
    def get_database_info(self):
        """
        获取数据库基本信息
        """
        print(f"操作的数据库类型: {self.db.dialect}")
        print(f"数据库中的表: {self.db.get_usable_table_names()}")
        
        # 可以选择获取每个表的结构信息
        tables = self.db.get_usable_table_names()
        for table in tables:
            print(f"\n表 {table} 的结构:")
            try:
                schema_info = self.db.run(f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table}'")
                print(schema_info)
            except Exception as e:
                print(f"获取表 {table} 结构时出错: {str(e)}")
    
    def create_sql_query(self, user_question):
        """
        根据用户问题生成SQL查询
        
        参数:
            user_question: 用户的自然语言问题
            
        返回:
            生成的SQL查询字符串
        """
        # 创建SQL查询链
        chain = create_sql_query_chain(self.llm, self.db)
        
        # 生成SQL查询
        query = chain.invoke({"question": user_question})
        return query
    
    def execute_query(self, query):
        """
        执行SQL查询
        
        参数:
            query: SQL查询语句
            
        返回:
            查询结果
        """
        try:
            result = self.db.run(query)
            return result
        except Exception as e:
            return f"执行查询时出错: {str(e)}"
    
    def ask_database(self, user_question):
        """
        完整的问答流程: 生成查询 -> 执行查询 -> 返回结果
        
        参数:
            user_question: 用户的自然语言问题
        """
        print(f"\n用户问题: {user_question}")
        
        # 生成SQL查询
        query = self.create_sql_query(user_question)
        print(f"\n生成的SQL查询:")
        print(query)
        
        # 执行查询
        result = self.execute_query(query)
        print(f"\n查询结果:")
        print(result)
        
        # 可以选择让LLM解释结果
        print(f"\n结果解释:")
        self.explain_result(user_question, query, result)
    
    def explain_result(self, question, query, result):
        """
        让LLM解释查询结果
        """
        explanation_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个数据分析专家，擅长解释SQL查询结果。请用自然、友好的语言解释结果，避免技术术语。"),
            ("human", "用户问题: {question}\n\n执行的SQL查询: {query}\n\n查询结果: {result}\n\n请解释这个结果如何回答了用户的问题。")
        ])
        
        explanation_chain = explanation_prompt | self.llm
        response = explanation_chain.invoke({
            "question": question,
            "query": query,
            "result": result
        })
        print(response.content)

def main():
    """
    主函数，演示PostgreSQL SQL查询工具的使用
    """
    print("=== PostgreSQL SQL查询工具 ===")
    print("本工具可以帮助你自动生成SQL查询并执行，基于你的自然语言问题")
    
    # 数据库连接信息
    # 注意：在实际使用时，建议将这些信息存储在环境变量中
    db_user = "postgres"  # PostgreSQL默认用户名
    db_password = "your_password"  # 请修改为你的密码
    db_host = "localhost"  # 或 127.0.0.1
    db_port = "5432"  # PostgreSQL默认端口
    db_database = "your_database"  # 请修改为你的数据库名
    
    try:
        # 创建工具实例
        pg_tool = PostgresSQLTool(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_database
        )
        
        # 获取数据库信息
        print("\n=== 数据库信息 ===")
        pg_tool.get_database_info()
        
        # 交互式问答
        print("\n=== 开始问答（输入'退出'结束）===")
        while True:
            question = input("\n请输入你的问题: ")
            if question.lower() in ['退出', 'exit', 'quit', 'q']:
                print("感谢使用，再见！")
                break
            
            pg_tool.ask_database(question)
            
    except Exception as e:
        print(f"\n连接数据库时出错: {str(e)}")
        print("请检查数据库连接信息是否正确，以及PostgreSQL服务是否正常运行。")
        print("注意：使用前请确保已安装psycopg2库: pip install psycopg2-binary")

if __name__ == "__main__":
    main()

"""
使用说明：

1. 安装必要的依赖:
   pip install -U langchain langchain-community langchain-openai psycopg2-binary

2. 修改数据库连接信息:
   - db_user: PostgreSQL用户名（默认为postgres）
   - db_password: 你的PostgreSQL密码
   - db_host: 数据库主机地址
   - db_port: PostgreSQL端口（默认为5432）
   - db_database: 你要连接的数据库名

3. 运行脚本:
   python pg_sql_query_tool.py

4. 在交互式界面中输入你的问题，工具会自动生成SQL查询并执行

注意事项:
- 确保PostgreSQL服务已启动
- 确保用户有权限访问指定的数据库
- 对于复杂查询，可能需要根据实际情况调整提示词或查询结果
- 生产环境中，建议使用环境变量存储敏感信息
"""