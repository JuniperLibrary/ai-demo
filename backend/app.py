from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import psycopg2
import json
import uuid
import re
import os
from dotenv import load_dotenv
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库连接管理
connections = {}

# 配置OpenAI API密钥
openai_api_key = os.environ.get('OPENAI_API_KEY', '')  # 从环境变量获取，或者设置默认值
llm = None

# 只有在有API密钥时才初始化OpenAI
if openai_api_key:
    try:
        llm = OpenAI(api_key=openai_api_key)
        print("OpenAI API客户端初始化成功")
    except Exception as e:
        print(f"OpenAI API初始化失败，但服务将继续运行（仅使用基础功能）: {e}")
        llm = None

# SQL生成提示模板
sql_prompt = PromptTemplate(
    input_variables=["query", "db_type", "schema_info"],
    template="""
    你是一个专业的SQL专家。请根据用户的查询需求和数据库表结构，生成正确的{db_type} SQL查询语句。
    
    数据库表结构信息:
    {schema_info}
    
    用户查询需求:
    {query}
    
    请只返回SQL查询语句，不要包含任何解释或其他内容。确保SQL语法正确，并且符合{db_type}的规范。
    """
)

# 获取数据库表结构
def get_database_schema(connection, db_type):
    try:
        cursor = connection.cursor()
        schema_info = []
        
        if db_type == 'mysql':
            # 获取所有表
            cursor.execute("SHOW TABLES")
            tables = [table[0] for table in cursor.fetchall()]
            
            # 获取每个表的结构
            for table in tables:
                cursor.execute(f"DESCRIBE {table}")
                columns = [col[0] for col in cursor.fetchall()]
                schema_info.append(f"表名: {table}, 字段: {', '.join(columns)}")
        
        elif db_type == 'postgresql':
            # 获取所有表
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = [table[0] for table in cursor.fetchall()]
            
            # 获取每个表的结构
            for table in tables:
                # 使用参数化查询避免SQL注入
                cursor.execute(
                    "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
                    (table,)
                )
                columns = [col[0] for col in cursor.fetchall()]
                schema_info.append(f"表名: {table}, 字段: {', '.join(columns)}")
        
        cursor.close()
        return "\n".join(schema_info)
    except Exception as e:
        return f"获取表结构失败: {str(e)}"

# 清理SQL查询
def clean_sql_query(sql_query):
    """清理生成的SQL查询，移除不需要的标记和格式"""
    # 移除常见的标记前缀
    sql_query = re.sub(r'^sql|^```sql|^```', '', sql_query, flags=re.IGNORECASE)
    # 移除常见的标记后缀
    sql_query = re.sub(r'```$', '', sql_query)
    # 清理前后空白
    sql_query = sql_query.strip()
    return sql_query

# 安全检查SQL查询
def validate_sql_query(sql_query):
    """验证SQL查询的安全性，确保只执行SELECT查询"""
    # 转换为大写进行安全检查
    sql_upper = sql_query.upper()
    
    # 检查是否包含危险操作
    dangerous_keywords = [
        'DROP', 'TRUNCATE', 'DELETE', 'UPDATE', 'INSERT',
        'ALTER', 'CREATE', 'RENAME', 'EXEC', 'EXECUTE',
        'GRANT', 'REVOKE', 'SHUTDOWN', 'KILL'
    ]
    
    for keyword in dangerous_keywords:
        # 使用单词边界检查以避免误报
        pattern = r'\\b' + keyword + r'\\b'
        if re.search(pattern, sql_upper):
            raise Exception(f"检测到潜在危险的SQL操作: {keyword}")
    
    # 检查是否只包含查询操作
    if not re.search(r'\\bSELECT\\b', sql_upper):
        raise Exception("只允许执行SELECT查询语句")
    
    # 检查是否包含多个语句（分号）
    if sql_upper.count(';') > 1:
        raise Exception("不允许执行多条SQL语句")
    
    return True

# 测试数据库连接
@app.route('/api/test-connection', methods=['POST'])
def test_connection():
    try:
        data = request.json
        db_type = data.get('type')
        host = data.get('host')
        port = data.get('port')
        database = data.get('database')
        username = data.get('username')
        password = data.get('password')
        
        connection = None
        
        if db_type == 'mysql':
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
        elif db_type == 'postgresql':
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                dbname=database
            )
        else:
            return jsonify({"success": False, "error": "不支持的数据库类型"})
        
        if connection.is_connected() if hasattr(connection, 'is_connected') else True:
            connection.close()
            return jsonify({"success": True, "message": "连接成功"})
        else:
            return jsonify({"success": False, "error": "连接失败"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 连接数据库
@app.route('/api/connect-db', methods=['POST'])
def connect_db():
    try:
        data = request.json
        db_type = data.get('type')
        host = data.get('host')
        port = data.get('port')
        database = data.get('database')
        username = data.get('username')
        password = data.get('password')
        
        connection = None
        
        if db_type == 'mysql':
            connection = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
        elif db_type == 'postgresql':
            connection = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                dbname=database
            )
        else:
            return jsonify({"success": False, "error": "不支持的数据库类型"})
        
        if connection.is_connected() if hasattr(connection, 'is_connected') else True:
            # 生成连接ID
            connection_id = str(uuid.uuid4())
            # 保存连接信息，包括密码以便后续使用
            connections[connection_id] = {
                'connection': connection,
                'type': db_type,
                'info': {
                    'host': host,
                    'port': port,
                    'database': database,
                    'username': username,
                    'password': password  # 安全地存储密码以用于后续操作
                }
            }
            return jsonify({
                "success": True, 
                "message": f"成功连接到 {db_type} 数据库: {database}",
                "connection_id": connection_id
            })
        else:
            return jsonify({"success": False, "error": "连接失败"})
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 获取数据库表信息
@app.route('/api/get-tables', methods=['POST'])
def get_tables():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        
        if connection_id not in connections:
            return jsonify({"success": False, "error": "无效的连接ID"})
        
        conn_info = connections[connection_id]
        connection = conn_info['connection']
        db_type = conn_info['type']
        
        cursor = connection.cursor()
        tables = []
        
        if db_type == 'mysql':
            cursor.execute("SHOW TABLES")
            table_names = [table[0] for table in cursor.fetchall()]
            
            for table in table_names:
                cursor.execute(f"DESCRIBE {table}")
                columns = [col[0] for col in cursor.fetchall()]
                tables.append({
                    'name': table,
                    'columns': columns
                })
        
        elif db_type == 'postgresql':
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            table_names = [table[0] for table in cursor.fetchall()]
            
            for table in table_names:
                # 使用参数化查询避免SQL注入
                cursor.execute(
                    "SELECT column_name FROM information_schema.columns WHERE table_name = %s",
                    (table,)
                )
                columns = [col[0] for col in cursor.fetchall()]
                tables.append({
                    'name': table,
                    'columns': columns
                })
        
        cursor.close()
        return jsonify({"success": True, "tables": tables})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 生成SQL查询
@app.route('/api/generate-sql', methods=['POST'])
def generate_sql():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        user_query = data.get('query')
        
        if connection_id not in connections:
            return jsonify({"success": False, "error": "无效的连接ID"})
        
        conn_info = connections[connection_id]
        connection = conn_info['connection']
        db_type = conn_info['type']
        
        # 获取数据库结构信息
        schema_info = get_database_schema(connection, db_type)
        
        # 如果没有OpenAI API密钥或初始化失败，使用简单的规则生成SQL（演示用）
        if not llm:
            # 简单的SQL生成逻辑（仅作为演示）
            if "查询" in user_query and "所有" in user_query and "表" in user_query:
                # 从查询中提取表名
                match = re.search(r'(\w+)表', user_query)
                if match:
                    table_name = match.group(1)
                    sql = f"SELECT * FROM {table_name}"
                    return jsonify({"success": True, "sql": sql})
            
            # 默认SQL
            sql = "SELECT * FROM information_schema.tables LIMIT 10"
            return jsonify({"success": True, "sql": sql, "warning": "使用基础SQL生成功能（未配置OpenAI API密钥）"})
        
        # 使用OpenAI生成SQL
        prompt = sql_prompt.format(
            query=user_query,
            db_type=db_type,
            schema_info=schema_info
        )
        
        try:
            # 调用OpenAI API生成SQL
            response = llm(prompt)
            generated_sql = response.strip()
            
            # 清理生成的SQL
            generated_sql = clean_sql_query(generated_sql)
            
            return jsonify({"success": True, "sql": generated_sql})
        except Exception as ai_error:
            # AI生成失败时提供更友好的错误信息
            return jsonify({
                "success": False, 
                "error": f"SQL生成失败: {str(ai_error)}. 请尝试重新描述您的查询需求。"
            })
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 执行SQL查询
@app.route('/api/execute-sql', methods=['POST'])
def execute_sql():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        sql = data.get('sql')
        
        if connection_id not in connections:
            return jsonify({"success": False, "error": "无效的连接ID"})
        
        conn_info = connections[connection_id]
        connection = conn_info['connection']
        
        # 验证SQL查询的安全性
        try:
            validate_sql_query(sql)
        except Exception as security_error:
            return jsonify({"success": False, "error": str(security_error)})
        
        cursor = connection.cursor()
        
        try:
            cursor.execute(sql)
            
            # 获取列名
            columns = [desc[0] for desc in cursor.description]
            
            # 获取数据行并确保可JSON序列化
            rows = []
            for row in cursor.fetchall():
                serializable_row = []
                for value in row:
                    if value is None:
                        serializable_row.append(None)
                    elif hasattr(value, 'isoformat'):
                        # 处理日期时间类型
                        serializable_row.append(value.isoformat())
                    else:
                        # 尝试直接转换为字符串
                        try:
                            # 先尝试转换为JSON看看是否会出错
                            json.dumps(value)
                            serializable_row.append(value)
                        except (TypeError, ValueError):
                            # 如果出错，转换为字符串
                            serializable_row.append(str(value))
                rows.append(serializable_row)
            
            # 限制返回的数据量
            max_rows = 1000  # 设置最大返回行数
            if len(rows) > max_rows:
                rows = rows[:max_rows]
                return jsonify({
                    "success": True, 
                    "results": {"columns": columns, "rows": rows},
                    "warning": f"结果超过{max_rows}行，仅显示前{max_rows}行"
                })
            
            return jsonify({
                "success": True, 
                "results": {"columns": columns, "rows": rows}
            })
            
        except Exception as sql_error:
            return jsonify({"success": False, "error": f"SQL执行失败: {str(sql_error)}"})
        finally:
            # 确保游标关闭
            if cursor:
                cursor.close()
                
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 关闭数据库连接
@app.route('/api/disconnect-db', methods=['POST'])
def disconnect_db():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        
        if connection_id not in connections:
            return jsonify({"success": False, "error": "无效的连接ID"})
        
        # 安全地关闭连接
        try:
            connection = connections[connection_id]['connection']
            if connection and (not hasattr(connection, 'closed') or not connection.closed):
                connection.close()
        except Exception as close_error:
            # 记录关闭错误但继续删除连接记录
            print(f"关闭连接时出错: {str(close_error)}")
        
        # 从字典中移除连接记录
        del connections[connection_id]
        
        return jsonify({"success": True, "message": "数据库连接已关闭"})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# 健康检查端点
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "message": "数据库AI助手后端服务运行正常"})

if __name__ == '__main__':
    # 使用环境变量中的端口，默认为5001
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)  # 生产环境中应设置debug=False
    print(f"后端服务已启动，监听端口: {port}")