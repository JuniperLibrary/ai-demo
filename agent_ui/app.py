from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import psycopg2
from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
import os

app = Flask(__name__)
CORS(app)  # 启用跨域支持

# 存储数据库连接
active_connections = {}

# 数据库连接测试
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
        
        if db_type == 'mysql':
            conn = mysql.connector.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                database=database
            )
            conn.close()
        elif db_type == 'postgresql':
            conn = psycopg2.connect(
                host=host,
                port=port,
                user=username,
                password=password,
                dbname=database
            )
            conn.close()
        else:
            return jsonify({'error': '不支持的数据库类型'}), 400
        
        return jsonify({'success': True, 'message': '连接成功'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# 建立数据库连接
@app.route('/api/connect-db', methods=['POST'])
def connect_db():
    try:
        data = request.json
        connection_id = f"{data['host']}:{data['port']}:{data['database']}"
        
        # 存储连接信息
        active_connections[connection_id] = data
        
        return jsonify({'success': True, 'connection_id': connection_id, 'message': f'成功连接到 {data["type"].upper()} 数据库: {data["database"]}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# 获取数据库表信息
@app.route('/api/get-tables', methods=['POST'])
def get_tables():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        
        if connection_id not in active_connections:
            return jsonify({'success': False, 'error': '未找到活动连接'}), 400
        
        conn_info = active_connections[connection_id]
        tables_info = []
        
        if conn_info['type'] == 'mysql':
            conn = mysql.connector.connect(
                host=conn_info['host'],
                port=conn_info['port'],
                user=conn_info['username'],
                password=conn_info['password'],
                database=conn_info['database']
            )
            cursor = conn.cursor()
            
            # 获取所有表名
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            for (table_name,) in tables:
                # 获取表结构
                cursor.execute(f"DESCRIBE {table_name}")
                columns = [column[0] for column in cursor.fetchall()]
                tables_info.append({'name': table_name, 'columns': columns})
            
            cursor.close()
            conn.close()
        elif conn_info['type'] == 'postgresql':
            conn = psycopg2.connect(
                host=conn_info['host'],
                port=conn_info['port'],
                user=conn_info['username'],
                password=conn_info['password'],
                dbname=conn_info['database']
            )
            cursor = conn.cursor()
            
            # 获取所有表名
            cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
            tables = cursor.fetchall()
            
            for (table_name,) in tables:
                # 获取表结构
                cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
                columns = [column[0] for column in cursor.fetchall()]
                tables_info.append({'name': table_name, 'columns': columns})
            
            cursor.close()
            conn.close()
        
        return jsonify({'success': True, 'tables': tables_info})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# 生成SQL查询
@app.route('/api/generate-sql', methods=['POST'])
def generate_sql():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        user_query = data.get('query')
        
        if connection_id not in active_connections:
            return jsonify({'success': False, 'error': '未找到活动连接'}), 400
        
        conn_info = active_connections[connection_id]
        
        # 创建数据库URL
        if conn_info['type'] == 'mysql':
            db_url = f"mysql+pymysql://{conn_info['username']}:{conn_info['password']}@{conn_info['host']}:{conn_info['port']}/{conn_info['database']}"
        elif conn_info['type'] == 'postgresql':
            db_url = f"postgresql://{conn_info['username']}:{conn_info['password']}@{conn_info['host']}:{conn_info['port']}/{conn_info['database']}"
        
        # 创建数据库实例
        db = SQLDatabase.from_uri(db_url)
        
        # 使用LangChain创建SQL查询链
        llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        chain = create_sql_query_chain(llm, db)
        
        # 生成SQL查询
        generated_sql = chain.invoke({"question": user_query})
        
        return jsonify({'success': True, 'sql': generated_sql})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# 执行SQL查询
@app.route('/api/execute-sql', methods=['POST'])
def execute_sql():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        sql = data.get('sql')
        
        if connection_id not in active_connections:
            return jsonify({'success': False, 'error': '未找到活动连接'}), 400
        
        conn_info = active_connections[connection_id]
        results = {"columns": [], "rows": []}
        
        if conn_info['type'] == 'mysql':
            conn = mysql.connector.connect(
                host=conn_info['host'],
                port=conn_info['port'],
                user=conn_info['username'],
                password=conn_info['password'],
                database=conn_info['database']
            )
            cursor = conn.cursor()
            
            # 执行查询
            cursor.execute(sql)
            
            # 获取列名
            results['columns'] = [desc[0] for desc in cursor.description]
            
            # 获取数据
            rows = cursor.fetchall()
            # 将所有值转换为字符串以确保JSON序列化
            results['rows'] = [[str(value) if value is not None else None for value in row] for row in rows]
            
            cursor.close()
            conn.close()
        elif conn_info['type'] == 'postgresql':
            conn = psycopg2.connect(
                host=conn_info['host'],
                port=conn_info['port'],
                user=conn_info['username'],
                password=conn_info['password'],
                dbname=conn_info['database']
            )
            cursor = conn.cursor()
            
            # 执行查询
            cursor.execute(sql)
            
            # 获取列名
            results['columns'] = [desc[0] for desc in cursor.description]
            
            # 获取数据
            rows = cursor.fetchall()
            # 将所有值转换为字符串以确保JSON序列化
            results['rows'] = [[str(value) if value is not None else None for value in row] for row in rows]
            
            cursor.close()
            conn.close()
        
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

# 断开数据库连接
@app.route('/api/disconnect-db', methods=['POST'])
def disconnect_db():
    try:
        data = request.json
        connection_id = data.get('connection_id')
        
        if connection_id in active_connections:
            del active_connections[connection_id]
            return jsonify({'success': True, 'message': '已断开数据库连接'})
        else:
            return jsonify({'success': False, 'error': '未找到活动连接'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    # 设置环境变量以避免内存泄漏警告
    os.environ['OMP_NUM_THREADS'] = '1'
    app.run(debug=True, host='0.0.0.0', port=5000)