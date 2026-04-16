from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage
from langsmith import traceable
from prompts import get_agent_prompt
from config import llm
from pydantic import BaseModel
from typing import List
import json

class Evaluation(BaseModel):
    score: float
    issues: List[str]

def evaluate_response(response_content: str) -> dict:
    """Simple but effective self-correction evaluator"""
    eval_prompt = f"""Evaluate the following customer service response on a scale from 0.0 to 1.0.

Criteria: Accuracy, Politeness, Clarity, Helpfulness, Professionalism.

Response:
{response_content}

Return ONLY a valid JSON object:
{{"score": 0.85, "issues": ["short list of issues if any"]}}
"""

    try:
        structured_llm = llm.with_structured_output(Evaluation)
        result = structured_llm.invoke(eval_prompt)
        return result.model_dump()
    except:
        return {"score": 0.75, "issues": ["Evaluation failed"]}


@traceable(name="agent_node")
def agent_node(state: MessagesState):
    # TODO: In Week 5 we will connect real Long-term Memory here
    long_term_facts = "No previous customer facts available yet."

    prompt = get_agent_prompt()
    chain = prompt | llm

    response = chain.invoke({
        "messages": state["messages"],
        "long_term_facts": long_term_facts
    })

    # Self-Correction Logic (Week 2 Core Feature)
    eval_result = evaluate_response(response.content)

    if eval_result.get("score", 0) < 0.82:
        print(f"⚠️ Low quality detected (score: {eval_result['score']}). Applying self-correction...")

        correction_prompt = f"""Previous response had the following issues: {eval_result.get('issues', [])}

Please provide a better, more accurate, polite, and professional response to the customer."""

        better_response = (prompt | llm).invoke({
            "messages": state["messages"] + [
                AIMessage(content=response.content),
                HumanMessage(content=correction_prompt)
            ],
            "long_term_facts": long_term_facts
        })
        return {"messages": [better_response]}

    return {"messages": [response]}