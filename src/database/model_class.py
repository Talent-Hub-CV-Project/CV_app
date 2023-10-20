from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base import Base
from src.database.prediction import Prediction


class ModelPredictionClass(Base):
    __tablename__ = "model_prediction_class"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    class_predictions: Mapped[list[Prediction]] = relationship(back_populates="prediction_class")

    def __repr__(self) -> str:
        return f"<ModelPredictionClass(id={self.id}, name={self.name})>"
