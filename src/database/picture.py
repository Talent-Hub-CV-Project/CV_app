from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.database.model_class import ModelPredictionClass
    from src.database import Prediction
    from src.database.point import Point


class Picture(Base):
    __tablename__ = "picture"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    image: Mapped[bytes] = mapped_column(nullable=False)
    prediction_class_id: Mapped[int] = mapped_column(nullable=False)
    prediction_class: Mapped['ModelPredictionClass'] = relationship("ModelPredictionClass", backref="pictures")
    prediction_probability: Mapped[float] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    predictions: Mapped[list['Prediction']] = relationship(
        "Prediction", back_populates="pictures"
    )
    point_id: Mapped[int] = mapped_column(ForeignKey("point.id"))
    point: Mapped['Point'] = relationship("Point", backref="pictures")

    def __repr__(self) -> str:
        return f"<Picture(id={self.id}, name={self.name})>"
