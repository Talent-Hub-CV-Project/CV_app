from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.database.model_class import ModelPredictionClass
    from src.database.picture import Picture


class Prediction(Base):
    __tablename__ = "prediction"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)

    picture_id: Mapped[int] = mapped_column(ForeignKey("picture.id"), index=True)
    picture: Mapped["Picture"] = relationship("Picture", backref="predictions")
    prediction_class_id: Mapped[int] = mapped_column(ForeignKey("model_prediction_class.id"), index=True)
    prediction_class: Mapped["ModelPredictionClass"] = relationship("ModelPredictionClass", backref="predictions")

    probability: Mapped[float] = mapped_column(nullable=False)
    box_x1: Mapped[float] = mapped_column(nullable=False)
    box_y1: Mapped[float] = mapped_column(nullable=False)
    box_x2: Mapped[float] = mapped_column(nullable=False)
    box_y2: Mapped[float] = mapped_column(nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Prediction(id={self.id}, picture_id={self.picture_id}, prediction_class={self.prediction_class},"
            f" probability={self.probability}, box_x1={self.box_x1}, box_y1={self.box_y1}, box_x2={self.box_x2},"
            f" box_y2={self.box_y2})>"
        )
