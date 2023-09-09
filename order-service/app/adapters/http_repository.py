from typing import Optional

import requests
from app.domain.model.checkout import Cart, Product
from app.domain.ports.repository import CartRepository, ProductRepository
from requests.adapters import HTTPAdapter, Retry


class HttpCartRepository(CartRepository):
    __retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[429, 502, 503, 504, 509]
    )

    def __init__(self, service_url: str) -> None:
        self.service_url = service_url
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=self.__retries))

    def get_cart(self, id: str) -> Optional[Cart]:
        response = self.session.get(
            f"http://{self.service_url}/cart", headers={"X-Session-ID": id}
        )
        response.raise_for_status()
        cart = Cart.parse_obj(response.json())

        return cart

    def empty_cart(self, id: str) -> None:
        response = self.session.delete(
            f"http://{self.service_url}/cart", headers={"X-Session-ID": id}
        )
        response.raise_for_status()


class HttpProductRepository(ProductRepository):
    __retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[429, 502, 503, 504, 509]
    )

    def __init__(self, service_url: str) -> None:
        self.service_url = service_url
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=self.__retries))

    def get_product(self, id: str) -> Optional[Product]:
        response = self.session.get(f"http://{self.service_url}/products/{id}")
        response.raise_for_status()
        product = Product.parse_obj(response.json())
        return product
