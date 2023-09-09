from typing import List, Optional

from app.adapters.models import pgsql_model
from app.domain.model import product
from app.domain.ports import repository
from sqlmodel import Session, select


class PgsqlProductRepository(repository.ProductRepository):
    def __init__(self, engine) -> None:
        self.__engine = engine

    def list_products(self) -> List[product.Product]:
        with Session(self.__engine) as session:
            statement = select(pgsql_model.Product)

            results = session.exec(statement)
            products = results.all()

        return products

    def get_product_by_id(self, product_id: int) -> Optional[product.Product]:
        with Session(self.__engine) as session:
            product = session.get(pgsql_model.Product, product_id)
        return product
