from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.model import product


class ProductRepository(ABC):
    @abstractmethod
    def list_products(self) -> List[product.Product]:
        ...

    @abstractmethod
    def get_product_by_id(self, product_id: str) -> Optional[product.Product]:
        ...
