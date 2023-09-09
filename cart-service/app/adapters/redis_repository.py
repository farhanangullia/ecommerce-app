import json
from typing import List, Optional

from app.domain.model.cart import Cart, CartItem
from app.domain.ports.repository import CartRepository
from redis import StrictRedis


class RedisCartRepository(CartRepository):
    _field = "cart"

    def __init__(self, redis_client: StrictRedis) -> None:
        self.__redis_client = redis_client

    def get_cart(self, key: str) -> Optional[Cart]:
        cart_items = self.__redis_client.hget(key, self._field)
        cart_items = json.loads(cart_items) if cart_items else []
        return Cart(items=cart_items)

    def add_to_cart(self, key: str, items: List[CartItem]) -> None:
        self.__redis_client.hset(
            key, self._field, json.dumps([i.dict() for i in items])
        )

    def delete_cart(self, key: str) -> None:
        self.__redis_client.hdel(key, self._field)
