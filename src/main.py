from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy import Connection
from sqlalchemy_utils import create_database, database_exists

from src.database.session_manager import SessionManager
from src.interface import create_interface
from src.repository.model_prediction import ModelClassRepo
from src.settings import Settings

settings = Settings()


def run_upgrade(connection: Connection, cfg: Config) -> None:
    cfg.attributes["connection"] = connection
    upgrade(cfg, "head")


def init_database() -> None:
    if not database_exists(settings.postgres_dsn):
        create_database(settings.postgres_dsn)
    config = Config("alembic.ini")
    config.attributes["configure_logger"] = False
    engine = SessionManager().engine
    with engine.connect() as conn:
        with conn.begin():
            run_upgrade(conn, config)
            conn.commit()
    ModelClassRepo.create_classes()


if __name__ == "__main__":
    init_database()
    interface = create_interface()
    interface.queue().launch()
