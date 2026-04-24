from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

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

@dataclass
class CustomerInput:
    customer_id: str
    message: str