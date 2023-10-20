from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.picture import Picture


class Point(Base):
    __tablename__ = "point"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    pictures: Mapped[list[Picture]] = relationship("Picture", back_populates="point_id")

    def __repr__(self) -> str:
        return f"<Point(id={self.id}, name={self.name})>"
