from langgraph.graph import MessagesState
from typing import Literal
from typing import List, Optional

from pydantic import BaseModel, Field


class Step(BaseModel):
    title: str = ""
    description: str = ""
    status: Literal["pending", "completed"] = "pending"


class Plan(BaseModel):
    goal: str = ""
    thought: str = ""
    steps: List[Step] = []
    
    # 允许像字典一样访问属性，支持代码中的字典访问方式
    def __getitem__(self, key):
        return getattr(self, key)
    
    def __setitem__(self, key, value):
        setattr(self, key, value)

class State(MessagesState):
    user_message: str = ""
    plan: Plan
    observations: List = []
    final_report: str =  ""
    