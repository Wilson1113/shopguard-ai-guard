from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore   # 开发用，后续换 PostgresStore
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI   # 或用 DeepSeek / Groq
from pydantic import BaseModel, Field
from typing import List
import os
from langchain_groq import ChatGroq

# Initialize the model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    api_key=os.getenv('GROQ_API_KEY')
)

# ====================== 1. 定义 State ======================
class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    user_id: str   # 用来区分不同用户


class UserFact(BaseModel):
    """A single piece of information about the user."""
    key: str = Field(description="The category or topic of the fact (e.g., 'birthday', 'location')")
    value: str = Field(description="The specific information found")

class FactExtraction(BaseModel):
    """The collection of all facts found in the text."""
    facts: List[UserFact]

# ====================== 2. 初始化 Store 和 Checkpointer ======================
store = InMemoryStore()                    # 开发测试用，重启会清空
checkpointer = MemorySaver()               # short-term memory

# ====================== 3. Long-term Memory 相关工具函数 ======================
def get_user_facts(store, user_id: str) -> dict:
    """Get the User Facts"""
    namespace = (user_id, "facts")         # namespace 示例：("user123", "facts")
    items = store.search(namespace, limit=10)
    facts = {}
    for item in items:
        facts[item.key] = item.value
    return facts

def save_user_fact(store, user_id: str, key: str, value: dict):
    """保存或更新一条用户事实到 Long-term Store"""
    namespace = (user_id, "facts")
    store.put(namespace, key, value)       # value 可以是任意 dict

# ====================== 4. Agent Node（注入 Long-term Memory） ======================

def agent_node(state: AgentState):
    user_id = state["user_id"]
    
    # 1. 检索 Long-term Memory
    long_term_facts = get_user_facts(store, user_id)
    facts_list = [f"- {k}: {v.get('value', v) if isinstance(v, dict) else v}" 
                  for k, v in long_term_facts.items()]
    facts_str = "\n".join(facts_list) if facts_list else "No previous facts."

    
    # 2. 构建带 Long-term Memory 的 Prompt
    system_prompt = f"""You are a helpful assistant.
You have the following long-term facts about the user:
{facts_str}

Use these facts to provide personalized responses when relevant.
If you learn new important facts about the user (preferences, background, etc.), remember them for future conversations."""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("placeholder", "{messages}"),
    ])

    chain = prompt | llm
    response = chain.invoke({"messages": state["messages"]})
    
    # 3. （可选）在回复后提取新事实并保存到 Long-term Memory
    # 这里用简单 LLM call 做提取，生产中可做得更精细
    extract_prompt = f"""From the latest conversation, extract any new important facts or preferences about the user.
Only output valid JSON like: {{"fact_key": "value"}} or empty dict if nothing new.

Conversation:
{state["messages"][-1].content}
Assistant: {response.content}
"""
    structured_llm = llm.with_structured_output(FactExtraction)
    extraction = structured_llm.invoke(extract_prompt)
    try:
        # 'extraction' is now a FactExtraction object, no eval() needed!
        for fact in extraction.facts:
            save_user_fact(store, user_id, fact.key, {
                "value": fact.value, 
                "updated_at": "now"
            })
    except:
        pass   # 提取失败就跳过
    
    return {"messages": [response]}

# ====================== 5. 构建 Graph ======================
workflow = StateGraph(AgentState)

workflow.add_node("agent", agent_node)

workflow.add_edge(START, "agent")
workflow.add_edge("agent", END)

# 关键：同时传入 checkpointer 和 store
graph = workflow.compile(
    checkpointer=checkpointer,
    store=store
)

# ====================== 6. 测试（演示 Long-term Memory） ======================
def run_conversation(user_id: str, query: str, thread_id: str):
    config = {"configurable": {"thread_id": thread_id}}
    input_state = {
        "messages": [HumanMessage(content=query)],
        "user_id": user_id
    }
    result = graph.invoke(input_state, config)
    print(f"User {user_id}: {query}")
    print(f"Assistant: {result['messages'][-1].content}\n")
    return result

# 测试流程
user_id = "wilson_001"

print("=== 第一轮对话（没有 Long-term Memory） ===")
run_conversation(user_id, "我喜欢用 bullet points 总结报告，而且我住在澳大利亚。", "session-1")
all_keys = store.search((user_id, "facts"))

print(all_keys)

print("=== 第二轮对话（不同 thread_id，但 Long-term Memory 已生效） ===")
run_conversation(user_id, "帮我总结一下 2026 AI Agent 的发展趋势。", "session-2")
all_keys = store.search((user_id, "facts"))

print(all_keys)

print("=== 第三轮对话（验证记忆是否被记住） ===")
run_conversation(user_id, "你还记得我之前的偏好吗？", "session-3")
all_keys = store.search((user_id, "facts"))

print(all_keys)