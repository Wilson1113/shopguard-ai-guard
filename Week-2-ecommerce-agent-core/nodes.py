from langgraph.graph import MessagesState
from langchain_core.messages import AIMessage, HumanMessage
from langsmith import traceable
from prompts import get_agent_prompt
from config import llm
from pydantic import BaseModel, Field
from typing import List, Optional
import json

# ====================== Structured Evaluator ======================
class ResponseEvaluation(BaseModel):
    """Structured evaluation result for self-correction"""
    score: float = Field(..., ge=0.0, le=1.0, description="Overall quality score 0.0-1.0")
    accuracy: float = Field(..., ge=0.0, le=1.0)
    politeness: float = Field(..., ge=0.0, le=1.0)
    clarity: float = Field(..., ge=0.0, le=1.0)
    helpfulness: float = Field(..., ge=0.0, le=1.0)
    issues: List[str] = Field(default_factory=list, description="Specific problems found")
    suggestion: Optional[str] = Field(None, description="Suggestion for improvement")

def evaluate_response_structured(response_content: str) -> ResponseEvaluation:
    """Use structured output for more reliable and detailed evaluation"""
    evaluation_prompt = f"""You are an expert evaluator for e-commerce customer service responses.

Evaluate the following response on multiple dimensions.

Response:
{response_content}

Provide a detailed evaluation in JSON format."""

    structured_llm = llm.with_structured_output(ResponseEvaluation)
    
    try:
        return structured_llm.invoke(evaluation_prompt)
    except Exception as e:
        print(f"Evaluation failed: {e}")
        # Fallback
        return ResponseEvaluation(
            score=0.75,
            accuracy=0.7,
            politeness=0.9,
            clarity=0.8,
            helpfulness=0.7,
            issues=["Evaluation error occurred"],
            suggestion="Please regenerate with more accuracy."
        )

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
    eval_result: ResponseEvaluation = evaluate_response_structured(response.content)

    print(f"Evaluation Score: {eval_result.score:.2f} | Issues: {len(eval_result.issues)}")
# Trigger self-correction if quality is insufficient
    if eval_result.score < 0.85 or len(eval_result.issues) > 1:
        print("🔄 Self-correction triggered - regenerating response...")

        correction_prompt = f"""Previous response had the following issues:
{chr(10).join([f"- {issue}" for issue in eval_result.issues])}

Suggestion: {eval_result.suggestion or 'Improve accuracy, clarity and helpfulness.'}

Please generate a significantly better, more professional, accurate and customer-friendly response."""

        # Second generation with correction context
        better_response = (prompt | llm).invoke({
            "messages": state["messages"] + [
                AIMessage(content=response.content),
                HumanMessage(content=correction_prompt)
            ],
            "long_term_facts": long_term_facts
        })
        
        final_eval = evaluate_response_structured(better_response.content)
        print(f"Corrected Score: {final_eval.score:.2f}")

        return {"messages": [better_response]}

    return {"messages": [response]}