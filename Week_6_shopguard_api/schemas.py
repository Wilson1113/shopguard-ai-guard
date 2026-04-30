from typing import List
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    thread_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str

class CustomerInput(BaseModel):
    customer_id: str
    message: str

class Order(BaseModel):
    order_id: str
    customer_id: str
    status: str
    total_amount: float
    created_at: datetime
    items: List[dict]

class Customer(BaseModel):
    customer_id: str
    name: str
    email: str
    country: str = "AU"
    preferences: Optional[dict] = None

class ProductInventory(BaseModel):
    product_id: str
    name: str
    stock_quantity: int
    price: float