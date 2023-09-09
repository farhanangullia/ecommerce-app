from typing import List

from app.domain.model.checkout import Order
from app.domain.ports.repository import OrderRepository


class OrderService:
    def __init__(
        self,
        order_repository: OrderRepository,
    ) -> None:
        self.__order_repository = order_repository

    def get_all_orders(self) -> List[Order]:
        return self.__order_repository.list_orders()

    def get_all_orders_by_customer_id(self, customer_id: str) -> List[Order]:
        return self.__order_repository.list_orders_by_customer(customer_id)

    def get_order(self, order_id: str) -> Order:
        return self.__order_repository.get_order(order_id)
