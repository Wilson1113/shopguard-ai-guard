from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage
from langsmith import traceable
from prompts import get_agent_prompt
from config import llm
from mcp_client import ShopMCPClient
import json
from pydantic import BaseModel, Field
from typing import List, Optional
from temporal_client import TemporalClient

class ResponseEvaluation(BaseModel):
    score: float = Field(..., ge=0.0, le=1.0)
    accuracy: float = Field(..., ge=0.0, le=1.0)
    politeness: float = Field(..., ge=0.0, le=1.0)
    clarity: float = Field(..., ge=0.0, le=1.0)
    helpfulness: float = Field(..., ge=0.0, le=1.0)
    issues: List[str] = Field(default_factory=list)
    suggestion: Optional[str] = Field(None)


@traceable(name="agent_node")
async def agent_node(state: MessagesState):
    user_id = "customer_001"

    # === Get the real time customer data through mcp ===
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

    # === Building a more natural System Prompt ===
    prompt = get_agent_prompt()
    chain = prompt | llm

    response = chain.invoke({
        "messages": state["messages"],
        "long_term_facts": long_term_facts
    })

    # === Trigger Long-Term Order Follow-up Workflow ===
    last_message = state["messages"][-1].content.lower()
    if "order" in last_message and ("status" in last_message or "arrived" in last_message or "delay" in last_message):
        try:
            temporal = TemporalClient()
            await temporal.trigger_order_followup("ORD-78492", user_id)
            response = AIMessage(content=response.content + "\n\n(I have started the order follow-up process for you and will continue to track it for you in the next few days.)")
        except Exception as e:
            print(f"Failed to trigger Temporal Workflow: {e}")

    # === Self-Correction ===
    eval_result = await evaluate_response_structured(response.content)

    print(f"📊 Evaluation Score: {eval_result.score:.2f}")

    if eval_result.score < 0.85 or len(eval_result.issues) > 1:
        print("🔄 Self-correction triggered...")

        correction_prompt = f"""The previous response was a bit too formal and repetitive.

Please rewrite it to sound more like a warm, natural, and caring customer service agent.
Show more empathy, use smoother transitions, and make the language more conversational.

Previous response: {response.content}"""

        better_response = (prompt | llm).invoke({
            "messages": state["messages"] + [
                AIMessage(content=response.content),
                HumanMessage(content=correction_prompt)
            ],
            "long_term_facts": long_term_facts
        })

        # === Trigger Long-Term Order Follow-up Workflow ===
        last_message = state["messages"][-1].content.lower()
        if "order" in last_message and ("status" in last_message or "arrived" in last_message or "delay" in last_message):
            try:
                temporal = TemporalClient()
                await temporal.trigger_order_followup("ORD-78492", user_id)
                better_response = AIMessage(content=better_response.content + "\n\n(I have started the order follow-up process for you and will continue to track it for you in the next few days.)")
            except Exception as e:
                print(f"Failed to trigger Temporal Workflow: {e}")
            return {"messages": [better_response]}

    return {"messages": [response]}


async def evaluate_response_structured(response_content: str) -> ResponseEvaluation:
    evaluation_prompt = f"""You are an expert evaluator for e-commerce customer service.

Evaluate this response:

Response:
{response_content}

Return ONLY a valid JSON object with the following fields:
{{
  "score": 0.92,
  "accuracy": 0.95,
  "politeness": 0.98,
  "clarity": 0.9,
  "helpfulness": 0.93,
  "issues": ["list any problems"],
  "suggestion": "optional suggestion"
}}
"""

    structured_llm = llm.with_structured_output(ResponseEvaluation)
    try:
        return structured_llm.invoke(evaluation_prompt)
    except:
        return ResponseEvaluation(
            score=0.8, accuracy=0.8, politeness=0.9, clarity=0.8, helpfulness=0.8,
            issues=["Could not evaluate"], suggestion="Make response more natural"
        )