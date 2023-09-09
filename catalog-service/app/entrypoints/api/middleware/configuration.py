from app.adapters.models import pgsql_model
from app.entrypoints.api.helpers.responses import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine, select


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
    products = None
    with Session(engine) as session:
        statement = select(pgsql_model.Product)
        results = session.exec(statement)
        products = results.first()

    if products:
        return engine

    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    p1 = pgsql_model.Product(
        name="Gameboy",
        description="This device is a great piece of nintendo nostalgia for gamers",
        price=50,
        image="",
    )
    p2 = pgsql_model.Product(
        name="Switch",
        description="Enjoy a flexible gaming experience on this powerful, versatile console.",
        price=200,
        image="",
    )
    p3 = pgsql_model.Product(
        name="Xbox Series X",
        description="The fastest, most powerful Xbox ever.",
        price=729,
        image="",
    )
    p4 = pgsql_model.Product(
        name="Playstation 5",
        description="Marvel at incredible graphics and experience new PS5 features.",
        price=850,
        image="",
    )

    with Session(engine) as session:
        session.add(p1)
        session.add(p2)
        session.add(p3)
        session.add(p4)
        session.commit()

    return engine


def configure_logging() -> None:
    pass
