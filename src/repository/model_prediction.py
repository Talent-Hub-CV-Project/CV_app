from sqlalchemy import func, select
from sqlalchemy.orm import Session
from ultralytics.engine.results import Results  # type: ignore[import-untyped]

from src.database import ModelPredictionClass, Picture, Prediction, get_sync_session
from src.logger import get_logger
from src.repository.model_classes import ModelClassRepo
from src.repository.point import PointRepo

logger = get_logger(__name__)


class PredictionRepo:
    @staticmethod
    def create_model_prediction(model_prediction: list[Results], point_id: int, session: Session | None = None) -> None:
        if not session:
            session = get_sync_session()
        logger.info("Creating model prediction")
        point = PointRepo.get_point_by_id(point_id, session)
        for prediction in model_prediction:
            img = prediction.orig_img.tobytes()
            name = prediction.path
            picture = Picture(name=name, image=img, picture_point=point)
            for box in prediction.boxes:
                logger.debug("Box: {}".format(box))
                prob = box.conf.tolist()[0]
                cls = box.cls.tolist()[0]
                class_pred = ModelClassRepo.get_model_prediction_class(cls, session)
                bbox = box.xyxy.tolist()
                if len(bbox) > 1:
                    logger.warning("More than one bbox found {}".format(bbox))
                x1, y1, x2, y2 = bbox[0]
                session.add(
                    Prediction(
                        probability=prob,
                        box_x1=x1,
                        box_y1=y1,
                        box_x2=x2,
                        box_y2=y2,
                        prediction_class=class_pred,
                        picture_predicted=picture,
                    )
                )
            session.commit()

    @staticmethod
    def load_predictions_at_point(point_id: int, session: Session | None = None) -> list[tuple[str, float, str]]:
        if not session:
            session = get_sync_session()
        query = (
            select(Picture.name.label("filename"), Prediction.probability, ModelPredictionClass.name.label("class"))
            .join(Picture)
            .where(Picture.point_id == point_id)
            .join(ModelPredictionClass)
        )
        return session.execute(query).all()

    @staticmethod
    def load_animals_at_point(point_id: int, session: Session | None = None) -> list[tuple[str, int]]:
        if not session:
            session = get_sync_session()
        query = (
            select(ModelPredictionClass.name, func.count(Prediction.id))
            .join(ModelPredictionClass)
            .join(Picture)
            .where(Picture.point_id == point_id)
            .group_by(ModelPredictionClass.name)
        )
        return session.execute(query).all()
