from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    workflow_triggered: bool = False

class CustomerInput(BaseModel):
    customer_id: str
    message: str