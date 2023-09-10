from app.adapters.models import pgsql_model
from app.entrypoints.api.helpers.responses import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, SQLModel, create_engine


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
    with Session(engine) as session:
        if pgsql_model.Product.metadata.tables[
            pgsql_model.Product.__tablename__
        ].exists(engine):
            return engine
        else:
            SQLModel.metadata.create_all(engine)
            p1 = pgsql_model.Product(
                name="Gameboy",
                description="This device is a great piece of nintendo nostalgia for gamers",
                price=50,
                image="https://s6.imgcdn.dev/Ockqq.jpg",
            )
            p2 = pgsql_model.Product(
                name="Switch",
                description="Enjoy a flexible gaming experience on this powerful, versatile console.",
                price=200,
                image="https://s6.imgcdn.dev/Ocy0u.jpg",
            )
            p3 = pgsql_model.Product(
                name="Xbox Series X",
                description="The fastest, most powerful Xbox ever.",
                price=729,
                image="https://s6.imgcdn.dev/Ocs4B.jpg",
            )
            p4 = pgsql_model.Product(
                name="Playstation 5",
                description="Marvel at incredible graphics and experience new PS5 features.",
                price=850,
                image="https://s6.imgcdn.dev/OcivN.jpg",
            )
            session.add_all([p1, p2, p3, p4])
            session.commit()

            return engine


def configure_logging() -> None:
    pass
