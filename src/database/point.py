from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.picture import Picture


class Point(Base):
    __tablename__ = "point"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    point_pictures: Mapped[list[Picture]] = relationship(back_populates="picture_point")

    def __repr__(self) -> str:
        return f"<Point(id={self.id}, name={self.name})>"
