from store import UserFact
from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage
from langsmith import traceable
from prompts import get_agent_prompt
from config import llm
from store import get_user_facts, save_user_fact
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


def evaluate_response_structured(response_content: str) -> ResponseEvaluation:
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
def agent_node(state: MessagesState):
    # === Long-term Memory Integration ===
    # For demo, we use a fixed user_id. In real project, extract from context or auth.
    user_id = "customer_001"  
    
    long_term_facts_dict = get_user_facts(user_id)
    facts_list = [f"- {k}: {v}" for k, v in long_term_facts_dict.items()]
    long_term_facts = "\n".join(facts_list) if facts_list else "No previous customer facts available."

    # === Agent Generation ===
    prompt = get_agent_prompt()
    chain = prompt | llm

    response = chain.invoke({
        "messages": state["messages"],
        "long_term_facts": long_term_facts
    })

    # === Enhanced Self-Correction ===
    eval_result: ResponseEvaluation = evaluate_response_structured(response.content)

    print(f"📊 Evaluation Score: {eval_result.score:.2f} | Issues: {len(eval_result.issues)}")

    if eval_result.score < 0.85 or len(eval_result.issues) > 1:
        print("🔄 Self-correction triggered...")

        correction_prompt = f"""Previous response had issues:
{chr(10).join([f"- {issue}" for issue in eval_result.issues])}

Suggestion: {eval_result.suggestion or 'Make it more accurate and helpful.'}

Please generate a much better response."""

        better_response = (prompt | llm).invoke({
            "messages": state["messages"] + [
                AIMessage(content=response.content),
                HumanMessage(content=correction_prompt)
            ],
            "long_term_facts": long_term_facts
        })

        # Save new facts from the conversation (simple extraction)
        save_new_facts(user_id, state["messages"][-1].content, better_response.content)
        
        return {"messages": [better_response]}

    # Save facts even on normal responses
    save_new_facts(user_id, state["messages"][-1].content, response.content)
    return {"messages": [response]}


def save_new_facts(user_id: str, user_message: str, assistant_message: str):
    """Simple fact extraction and saving"""
    extract_prompt = f"""From the following conversation, extract any new important customer facts or preferences.
Only return valid JSON like: {{"preference": "value", "fact": "value"}}

Customer: {user_message}
Agent: {assistant_message}
"""

    try:
        structured_llm = llm.with_structured_output(UserFact)
        result = structured_llm.invoke(extract_prompt)
        for key, value in result.model_dump.items():
            save_user_fact(user_id, key, value)
    except:
        pass  # Fail silently in demo