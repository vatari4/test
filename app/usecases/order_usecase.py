from app.repositories.order_repository import OrderRepository

class OrderUseCase:
    def __init__(self, repo: OrderRepository):
        self.repo = repo

    async def add_item(self, order_id: int, product_id: int, quantity: int):
        return await self.repo.add_order_item(order_id, product_id, quantity)
