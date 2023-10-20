from alembic.config import Config
from alembic.command import upgrade
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy import Engine

from src.database.session_manager import SessionManager
from src.settings import Settings

settings = Settings()


def run_upgrade(connection: Engine, cfg: Config) -> None:
    cfg.attributes["connection"] = connection
    upgrade(cfg, "head")


def init_database():
    print(settings.postgres_dsn)
    if not database_exists(settings.postgres_dsn):
        create_database(settings.postgres_dsn)
    config = Config("alembic.ini")
    config.attributes["configure_logger"] = False
    engine = SessionManager().engine
    with engine.begin() as conn:
        run_upgrade(conn, config)
        # conn.run(run_upgrade, config)


if __name__ == "__main__":
    init_database()
