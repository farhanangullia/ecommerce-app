import logging
import os
from uuid import UUID

import uvicorn
from app.adapters.http_repository import HttpCartRepository, HttpProductRepository
from app.adapters.pgsql_repository import PgsqlOrderRepository
from app.domain.services.checkout import CartIsEmptyException, CheckoutService
from app.domain.services.order import OrderService
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

DB_URI = os.getenv("DB_URI")
CART_SERVICE_URL = os.getenv("CART_SERVICE_URL")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL")

engine = init(db_uri=DB_URI)


# Map ports and adapters
def make_checkout_controller() -> CheckoutService:
    order_repository = PgsqlOrderRepository(engine=engine)
    cart_repository = HttpCartRepository(service_url=CART_SERVICE_URL)
    product_repository = HttpProductRepository(service_url=PRODUCT_SERVICE_URL)
    return CheckoutService(
        order_repository=order_repository,
        cart_repository=cart_repository,
        product_repository=product_repository,
    )


def make_order_controller() -> OrderService:
    order_repository = PgsqlOrderRepository(engine=engine)
    return OrderService(order_repository=order_repository)


@app.post("/checkout")
def checkout(
    x_session_id: str = Header(None),
    controller: CheckoutService = Depends(make_checkout_controller),
):
    try:
        logger.info("checkout")
        if not x_session_id:
            return response_bad_request()

        order = controller.place_order(customer_id=x_session_id)
        logger.info(f"controller order: {order}")

        response = CheckoutResponse(
            order_id=str(order.id),
            created_on=order.created_on,
            total_amount=order.total_amount,
        )
        logger.info(response)

        return response_success(content=response.dict())
    except CartIsEmptyException:
        return response_bad_request()
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


@app.get("/orders")
def get_orders(
    x_session_id: str = Header(None),
    controller: OrderService = Depends(make_order_controller),
):
    try:
        logger.info("get_orders")
        if not x_session_id:
            return response_bad_request()

        orders = controller.get_all_orders_by_customer_id(customer_id=x_session_id)
        logger.info(f"controller orders: {orders}")
        orders_parsed = [Order.parse_obj(o.dict()) for o in orders]
        logger.info(f"parsed: {orders_parsed}")
        response = GetOrdersResponse(orders=orders_parsed)

        logger.info(response)

        return response_success(response.dict())
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


@app.get("/orders/{order_id}")
def get_order(
    order_id: UUID, controller: OrderService = Depends(make_order_controller)
):
    try:
        order = controller.get_order(order_id)
        logger.info(order)

        if not order:
            return response_not_found()

        response = GetOrderResponse.parse_obj(order)
        logger.info(response)

        return response_success(response.dict())
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
