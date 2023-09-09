from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.model.cart import Cart, CartItem


class CartRepository(ABC):
    @abstractmethod
    def get_cart(self, key: str) -> Optional[Cart]:
        ...

    @abstractmethod
    def add_to_cart(self, key: str, items: List[CartItem]) -> None:
        ...

    @abstractmethod
    def delete_cart(self, key: str) -> None:
        ...
