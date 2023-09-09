import uuid
from datetime import datetime

from app.domain.model.checkout import Cart, Order
from app.domain.ports.repository import (
    CartRepository,
    OrderRepository,
    ProductRepository,
)


class CartIsEmptyException(Exception):
    pass


class CheckoutService:
    def __init__(
        self,
        order_repository: OrderRepository,
        cart_repository: CartRepository,
        product_repository: ProductRepository,
    ) -> None:
        self.__order_repository = order_repository
        self.__cart_repository = cart_repository
        self.__product_repository = product_repository

    def prepare_order(self, customer_id: str) -> Order:
        order_id = uuid.uuid4()
        order_date = datetime.now()
        total_amount = 0

        cart = self.get_user_cart(customer_id)

        if not cart.items:
            raise CartIsEmptyException

        for item in cart.items:
            product = self.get_product(item.id)
            total_amount += item.count * product.price

        order = Order(
            id=order_id,
            created_on=order_date,
            customer_id=customer_id,
            total_amount=total_amount,
        )

        return order

    def create_order(self, order: Order) -> None:
        self.__order_repository.create_order(order)

    def place_order(self, customer_id: str) -> Order:
        order = self.prepare_order(customer_id)
        self.create_order(order)
        self.empty_cart(customer_id)
        return order

    def empty_cart(self, customer_id: str) -> None:
        return self.__cart_repository.empty_cart(customer_id)

    def get_user_cart(self, id: str) -> Cart:
        return self.__cart_repository.get_cart(id)

    def get_product(self, id: int) -> Order:
        return self.__product_repository.get_product(id)
