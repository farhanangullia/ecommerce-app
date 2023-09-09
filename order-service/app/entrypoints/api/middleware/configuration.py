from app.entrypoints.api.helpers.responses import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine


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


def init(db_uri: str):
    engine = create_engine(db_uri, echo=True)
    SQLModel.metadata.create_all(engine)

    return engine


def configure_logging() -> None:
    pass
