import json
import logging
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.types import Command
from langchain_openai import ChatOpenAI
from state import State
from prompts import *
from tools import *

# 从环境变量获取API密钥，避免硬编码
api_key = os.environ.get('DASHSCOPE_API_KEY', '')
llm = ChatOpenAI(model="deepseek-v3.1", temperature=0.0, base_url='https://dashscope.aliyuncs.com/compatible-mode/v1', api_key=api_key)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
hander = logging.StreamHandler()
hander.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hander.setFormatter(formatter)
logger.addHandler(hander)

def extract_json(text):
    if '```json' not in text:
        return text
    text = text.split('```json')[1].split('```')[0].strip()
    return text

def extract_answer(text):
    if '</think>' in text:
        answer = text.split("</think>")[-1]
        return answer.strip()
    
    return text

def create_planner_node(state: State):
    logger.info("***正在运行Create Planner node***")
    messages = [SystemMessage(content=PLAN_SYSTEM_PROMPT), HumanMessage(content=PLAN_CREATE_PROMPT.format(user_message = state['user_message']))]
    response = llm.invoke(messages)
    response = response.model_dump_json(indent=4, exclude_none=True)
    response = json.loads(response)
    plan = json.loads(extract_json(extract_answer(response['content'])))
    state['messages'] += [AIMessage(content=json.dumps(plan, ensure_ascii=False))]
    return Command(goto="execute", update={"plan": plan})

def update_planner_node(state: State):
    logger.info("***正在运行Update Planner node***")
    plan = state['plan']
    goal = plan['goal']
    state['messages'].extend([SystemMessage(content=PLAN_SYSTEM_PROMPT), HumanMessage(content=UPDATE_PLAN_PROMPT.format(plan = plan, goal=goal))])
    messages = state['messages']
    while True:
        try:
            response = llm.invoke(messages)
            response = response.model_dump_json(indent=4, exclude_none=True)
            response = json.loads(response)
            plan = json.loads(extract_json(extract_answer(response['content'])))
            state['messages']+=[AIMessage(content=json.dumps(plan, ensure_ascii=False))]
            return Command(goto="execute", update={"plan": plan})
        except Exception as e:
            messages += [HumanMessage(content=f"json格式错误:{e}")]
            
def execute_node(state: State):
    logger.info("***正在运行execute_node***")
  
    plan = state['plan']
    steps = plan['steps']
    current_step = None
    current_step_index = 0
    
    # 获取第一个未完成STEP
    for i, step in enumerate(steps):
        status = step['status']
        if status == 'pending':
            current_step = step
            current_step_index = i
            break
        
    logger.info(f"当前执行STEP:{current_step}")
    
    ## 此处只是简单跳转到report节点，实际应该根据当前STEP的描述进行判断
    if current_step is None or current_step_index == len(steps)-1:
        return Command(goto='report')
    
    messages = state['observations'] + [SystemMessage(content=EXECUTE_SYSTEM_PROMPT), HumanMessage(content=EXECUTION_PROMPT.format(user_message=state['user_message'], step=current_step['description']))]
    
    tool_result = None
    # 为Qwen模型准备工具信息
    tools = {"create_file": create_file, "str_replace": str_replace, "shell_exec": shell_exec}
    
    # 构建工具描述，添加到系统提示中
    tool_descriptions = []
    for tool_name, tool_func in tools.items():
        tool_descriptions.append(f"{tool_name}: {tool_func.__doc__}")
    
    # 添加工具调用格式说明到消息中
    tool_format_prompt = f"""
        请在需要调用工具时，使用以下格式输出：
        <tool_call>
        {{
          "name": "工具名称",
          "args": {{"参数名": "参数值"}}
        }}
        </tool_call>
        
        可用工具：
        {"\n".join(tool_descriptions)}
        """
    
    # 在消息列表开头添加工具格式说明
    messages_with_tools = [SystemMessage(content=tool_format_prompt)] + messages
    
    while True:
        try:
            # 不使用bind_tools，直接调用模型
            response = llm.invoke(messages_with_tools)
            response = response.model_dump_json(indent=4, exclude_none=True)
            response = json.loads(response)
            
            # 检查是否包含工具调用
            if '<tool_call>' in response['content']:
                try:
                    tool_call = response['content'].split('<tool_call>')[-1].split('</tool_call>')[0].strip()
                    tool_call = json.loads(tool_call)
                    
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']
                    
                    if tool_name in tools:
                        tool_result = tools[tool_name].invoke(tool_args)
                        logger.info(f"tool_name:{tool_name},tool_args:{tool_args}\ntool_result:{tool_result}")
                        messages_with_tools += [AIMessage(content=extract_answer(response['content']))]
                        messages_with_tools += [HumanMessage(content=f"工具执行结果: {json.dumps(tool_result, ensure_ascii=False)}")] 
                    else:
                        logger.error(f"未知工具: {tool_name}")
                        messages_with_tools += [AIMessage(content=extract_answer(response['content']))]
                        messages_with_tools += [HumanMessage(content=f"错误: 未知工具 '{tool_name}'")] 
                except Exception as e:
                    logger.error(f"工具调用解析错误: {str(e)}")
                    messages_with_tools += [AIMessage(content=extract_answer(response['content']))]
                    messages_with_tools += [HumanMessage(content=f"错误: 工具调用格式不正确 - {str(e)}")] 
            else:
                # 没有工具调用，直接返回结果
                break
        except Exception as e:
            logger.error(f"LLM调用失败: {str(e)}")
            # 添加错误信息到消息中，继续尝试
            messages_with_tools += [HumanMessage(content=f"请求失败，请重试: {str(e)}")]
            # 限制重试次数
            if len(messages_with_tools) > 20:
                break
        
    # 更新当前步骤状态为已完成
    if current_step:
        plan['steps'][current_step_index]['status'] = 'completed'
        
    logger.info(f"当前STEP执行总结:{extract_answer(response['content'])}")
    state['messages'] += [AIMessage(content=extract_answer(response['content']))]
    state['observations'] += [AIMessage(content=extract_answer(response['content']))]
    return Command(goto='update_planner', update={'plan': plan})
    

    
def report_node(state: State):
    """Report node that write a final report."""
    logger.info("***正在运行report_node***")
    
    observations = state.get("observations")
    messages = observations + [SystemMessage(content=REPORT_SYSTEM_PROMPT)]
    
    # 为Qwen模型准备工具信息
    tools = {"create_file": create_file, "shell_exec": shell_exec}
    
    # 构建工具描述，添加到系统提示中
    tool_descriptions = []
    for tool_name, tool_func in tools.items():
        tool_descriptions.append(f"{tool_name}: {tool_func.__doc__}")
    
    # 添加工具调用格式说明到消息中
    tool_format_prompt = f"""
        请在需要调用工具时，使用以下格式输出：
        <tool_call>
        {{
          "name": "工具名称",
          "args": {{"参数名": "参数值"}}
        }}
        </tool_call>
        
        可用工具：
        {"\n".join(tool_descriptions)}
        """
    
    # 在消息列表开头添加工具格式说明
    messages_with_tools = [SystemMessage(content=tool_format_prompt)] + messages
    
    while True:
        try:
            # 不使用bind_tools，直接调用模型
            response = llm.invoke(messages_with_tools)
            response = response.model_dump_json(indent=4, exclude_none=True)
            response = json.loads(response)
            
            # 检查是否包含工具调用
            if '<tool_call>' in response['content']:
                try:
                    tool_call = response['content'].split('<tool_call>')[-1].split('</tool_call>')[0].strip()
                    tool_call = json.loads(tool_call)
                    
                    tool_name = tool_call['name']
                    tool_args = tool_call['args']
                    
                    if tool_name in tools:
                        tool_result = tools[tool_name].invoke(tool_args)
                        logger.info(f"tool_name:{tool_name},tool_args:{tool_args}\ntool_result:{tool_result}")
                        messages_with_tools += [AIMessage(content=extract_answer(response['content']))]
                        messages_with_tools += [HumanMessage(content=f"工具执行结果: {json.dumps(tool_result, ensure_ascii=False)}")] 
                    else:
                        logger.error(f"未知工具: {tool_name}")
                        messages_with_tools += [AIMessage(content=extract_answer(response['content']))]
                        messages_with_tools += [HumanMessage(content=f"错误: 未知工具 '{tool_name}'")] 
                except Exception as e:
                    logger.error(f"工具调用解析错误: {str(e)}")
                    messages_with_tools += [AIMessage(content=extract_answer(response['content']))]
                    messages_with_tools += [HumanMessage(content=f"错误: 工具调用格式不正确 - {str(e)}")] 
            else:
                # 没有工具调用，直接返回结果
                break
        except Exception as e:
            logger.error(f"LLM调用失败: {str(e)}")
            # 添加错误信息到消息中，继续尝试
            messages_with_tools += [HumanMessage(content=f"请求失败，请重试: {str(e)}")]
            # 限制重试次数
            if len(messages_with_tools) > 20:
                break
            
    return {"final_report": response['content']}



