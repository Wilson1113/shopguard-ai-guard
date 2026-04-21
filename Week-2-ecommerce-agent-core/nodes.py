from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage
from langsmith import traceable
from prompts import get_agent_prompt
from config import llm
from mcp_client import ShopMCPClient
import json
from pydantic import BaseModel, Field
from typing import List, Optional

class ResponseEvaluation(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    accuracy: float = Field(..., ge=0.0, le=1.0)
    politeness: float = Field(..., ge=0.0, le=1.0)
    clarity: float = Field(..., ge=0.0, le=1.0)
    helpfulness: float = Field(..., ge=0.0, le=1.0)
    issues: List[str] = Field(default_factory=list)
    suggestion: Optional[str] = Field(None)


async def evaluate_response_structured(response_content: str) -> ResponseEvaluation:
    evaluation_prompt = f"""Evaluate this e-commerce customer service response:

Response:
{response_content}

Return a structured evaluation."""

    structured_llm = llm.with_structured_output(ResponseEvaluation)
    try:
        return structured_llm.invoke(evaluation_prompt)
    except:
        return ResponseEvaluation(
            score=0.75, accuracy=0.7, politeness=0.9, clarity=0.8, helpfulness=0.7,
            issues=["Evaluation failed"], suggestion="Regenerate with better accuracy."
        )


@traceable(name="agent_node")
async def agent_node(state: MessagesState):   # 注意改为 async
    user_id = "customer_001"

    # 通过 MCP 获取 Long-term + 当前订单/客户数据
    async with ShopMCPClient() as mcp:
        try:
            customer = await mcp.get_customer(user_id)
            long_term_facts = f"""
    Customer Name: {customer.get('name', 'Unknown')}
    Country: {customer.get('country', 'Unknown')}
    Preferences: {customer.get('preferences', {})}
    """
            print(f"✅ MCP Success: Got customer data for {user_id}")
            print(f"   Name: {customer.get('name')}")
            print(f"   Preferences: {customer.get('preferences')}")
        except Exception as e:
            long_term_facts = "No customer data available from MCP."
            print(f"❌ MCP Failed: {e}")

    prompt = get_agent_prompt()
    chain = prompt | llm

    response = chain.invoke({
        "messages": state["messages"],
        "long_term_facts": long_term_facts
    })

    # Self-Correction
    eval_result = await evaluate_response_structured(response.content)

    print(f"📊 Evaluation Score: {eval_result.score:.2f}")

    if eval_result.score < 0.85 or len(eval_result.issues) > 1:
        print("🔄 Self-correction triggered...")

        correction_prompt = f"""Previous response had issues: {eval_result.issues}
Suggestion: {eval_result.suggestion or 'Improve accuracy and helpfulness.'}

Please generate a better response."""

        better_response = (prompt | llm).invoke({
            "messages": state["messages"] + [
                AIMessage(content=response.content),
                HumanMessage(content=correction_prompt)
            ],
            "long_term_facts": long_term_facts
        })

        return {"messages": [better_response]}

    return {"messages": [response]}