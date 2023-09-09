import redis
from app.entrypoints.api.helpers.responses import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import StrictRedis


def configure_cors(app: FastAPI) -> None:
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def configure_health_checks(app: FastAPI) -> None:
    @app.get("/healthz")
    def get_health():
        return response_success(message="Health OK")


def init(redis_host: str, redis_port: int) -> StrictRedis:
    redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0)

    return redis_client


def configure_logging() -> None:
    pass
