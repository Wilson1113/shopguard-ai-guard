from pydantic import BaseModel

class CustomerInput(BaseModel):
    customer_id: str
    message: str