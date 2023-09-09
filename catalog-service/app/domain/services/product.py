from typing import List, Optional

from app.domain.model import product
from app.domain.ports import repository


class ProductService:
    def __init__(self, product_repository: repository.ProductRepository) -> None:
        self.__product_repository = product_repository

    def get_all(self) -> List[product.Product]:
        return self.__product_repository.list_products()

    def get(self, product_id: int) -> Optional[product.Product]:
        return self.__product_repository.get_product_by_id(product_id)
