from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.model.checkout import Cart, Order, Product


class OrderRepository(ABC):
    @abstractmethod
    def create_order(self, order: Order) -> None:
        ...

    @abstractmethod
    def list_orders(self) -> List[Order]:
        ...

    @abstractmethod
    def list_orders_by_customer(self, id: str) -> List[Order]:
        ...

    @abstractmethod
    def get_order(self, id: str) -> Optional[Order]:
        ...


class CartRepository(ABC):
    @abstractmethod
    def get_cart(self, id: str) -> Optional[Cart]:
        ...

    @abstractmethod
    def empty_cart(self, id: str) -> None:
        ...


class ProductRepository(ABC):
    @abstractmethod
    def get_product(self, id: str) -> Optional[Product]:
        ...


class ShippingRepository(ABC):
    @abstractmethod
    def create_shipping(
        self, address: str, country: str, total_amount: float, order_id: str
    ) -> str:
        ...
