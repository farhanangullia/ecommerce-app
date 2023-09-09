import logging
import os
import uuid

import uvicorn
from app.adapters.redis_repository import RedisCartRepository
from app.domain.model.cart import Product
from app.domain.services.cart import CartService
from app.entrypoints.api.helpers.responses import *
from app.entrypoints.api.middleware.configuration import (
    configure_cors,
    configure_health_checks,
    init,
)
from app.entrypoints.api.model.api_model import *
from fastapi import Depends, FastAPI, Header

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = FastAPI()

configure_cors(app)
configure_health_checks(app)

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

redis_client = init(redis_host=REDIS_HOST, redis_port=REDIS_PORT)


# Map ports and adapters
def make_cart_controller() -> CartService:
    repository = RedisCartRepository(redis_client=redis_client)
    return CartService(cart_repository=repository)


@app.get("/cart")
def get_cart(
    x_session_id: str = Header(None),
    controller: CartService = Depends(make_cart_controller),
):
    try:
        logger.info("get_cart")
        if not x_session_id:
            return response_bad_request()

        cart = controller.get_cart(x_session_id)
        logger.info(f"controller cart: {cart}")

        response = GetCartResponse.parse_obj(cart.dict())
        logger.info(response)

        return response_success(response.dict())
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


@app.put("/cart")
def add_to_cart(
    add_to_cart_request: AddToCartRequest,
    x_session_id: str = Header(None),
    controller: CartService = Depends(make_cart_controller),
):
    try:
        logger.info("add_to_cart")
        if not x_session_id:
            return response_bad_request()

        product = Product.parse_obj(add_to_cart_request.dict())
        logger.info(f"product: {product}")
        controller.add_to_cart(x_session_id, product)
        logger.info("added to cart")

        return response_success()
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


@app.delete("/cart")
def delete_cart(
    x_session_id: str = Header(None),
    controller: CartService = Depends(make_cart_controller),
):
    try:
        logger.info("delete_cart")
        if not x_session_id:
            return response_bad_request()

        controller.delete_cart(x_session_id)

        logger.info("Deleted cart...")

        return response_success()
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


@app.post("/cart/session")
def generate_session():
    session_id = str(uuid.uuid4())
    headers = {
        "X-Session-ID": session_id,
        "Access-Control-Expose-Headers": "X-Session-ID",
    }
    return response_success(headers=headers)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
