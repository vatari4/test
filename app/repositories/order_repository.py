from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.db.models import OrderItem, Product

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_product(self, product_id: int):
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        return result.scalar_one_or_none()

    async def get_order_item(self, order_id: int, product_id: int):
        result = await self.session.execute(
            select(OrderItem).where(OrderItem.order_id == order_id, OrderItem.product_id == product_id)
        )
        return result.scalar_one_or_none()

    async def add_order_item(self, order_id: int, product_id: int, quantity: int):
        order_item = await self.get_order_item(order_id, product_id)
        product = await self.get_product(product_id)

        if not product or product.quantity < quantity:
            raise ValueError("Not enough stock")

        if order_item:
            order_item.quantity += quantity
        else:
            order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
            self.session.add(order_item)

        product.quantity -= quantity
        await self.session.commit()
        return order_item
