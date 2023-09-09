from typing import Optional

from app.domain.model.cart import Cart, CartItem, Product
from app.domain.ports.repository import CartRepository


class CartService:
    def __init__(self, cart_repository: CartRepository) -> None:
        self.__cart_repository = cart_repository

    def get_cart(self, key: str) -> Optional[Cart]:
        return self.__cart_repository.get_cart(key)

    def add_to_cart(self, key: str, product: Product) -> None:
        cart = self.__cart_repository.get_cart(key)
        existing_item = next((i for i in cart.items if i.id == product.id), None)
        if existing_item:
            existing_item.count += 1
        else:
            new_cart_item = CartItem(**product.dict(), count=1)
            cart.items.append(new_cart_item)

        return self.__cart_repository.add_to_cart(key, cart.items)

    def delete_cart(self, key: str) -> None:
        return self.__cart_repository.delete_cart(key)
