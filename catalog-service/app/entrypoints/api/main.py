import logging
import os

import uvicorn
from app.adapters.pgsql_repository import PgsqlProductRepository
from app.domain.services.product import ProductService
from app.entrypoints.api.helpers.responses import *
from app.entrypoints.api.middleware.configuration import (
    configure_cors,
    configure_health_checks,
    init,
)
from app.entrypoints.api.model.api_model import *
from fastapi import Depends, FastAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

app = FastAPI()

configure_cors(app)
configure_health_checks(app)

DB_URI = os.getenv("DB_URI")

engine = init(db_uri=DB_URI)


# Map ports and adapters
def make_product_controller():
    repository = PgsqlProductRepository(engine=engine)
    return ProductService(product_repository=repository)


@app.get("/products")
def get_products(controller: ProductService = Depends(make_product_controller)):
    try:
        logger.info("get_products")
        products = controller.get_all()
        logger.info(f"controller products: {products}")
        products_parsed = [Product.parse_obj(p.dict()) for p in products]
        logger.info(f"parsed: {products_parsed}")
        response = GetProductsResponse(products=products_parsed)

        logger.info(response)

        return response_success(response.dict())
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


@app.get("/products/{product_id}")
def get_product(
    product_id: int, controller: ProductService = Depends(make_product_controller)
):
    try:
        product = controller.get(product_id)
        logger.info(product)

        if not product:
            return response_not_found()

        response = GetProductResponse.parse_obj(product)
        logger.info(response)

        return response_success(response.dict())
    except Exception as e:
        logger.error(e, exc_info=True)
        return response_error(err=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
