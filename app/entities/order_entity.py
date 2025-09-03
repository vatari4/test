from pydantic import BaseModel

class AddOrderItemRequest(BaseModel):
    order_id: int
    product_id: int
    quantity: int
