from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.settings import Settings


class SessionManager:
    """
    A class that implements the necessary functionality for working with the database:
    issuing sessions, storing and updating connection settings.
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls, is_async: bool = True) -> "SessionManager":
        if not hasattr(cls, "instance"):
            cls.instance = super().__new__(cls)
        return cls.instance  # noqa

    def get_session_maker(self) -> sessionmaker[Session]:
        return sessionmaker(self.engine, expire_on_commit=False, autoflush=False)

    def refresh(self) -> None:
        self.engine = create_engine(Settings().postgres_dsn, echo=True)


def get_sync_session() -> Session:
    session_maker = SessionManager().get_session_maker()
    with session_maker() as session:
        return session
