from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.entities.order_entity import AddOrderItemRequest
from app.repositories.order_repository import OrderRepository
from app.usecases.order_usecase import OrderUseCase

router = APIRouter()

@router.post("/orders/add-item")
async def add_item(request: AddOrderItemRequest, session: AsyncSession = Depends(get_session)):
    repo = OrderRepository(session)
    usecase = OrderUseCase(repo)
    try:
        order_item = await usecase.add_item(request.order_id, request.product_id, request.quantity)
        return {"order_id": order_item.order_id, "product_id": order_item.product_id, "quantity": order_item.quantity}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
