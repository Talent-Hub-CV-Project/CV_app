from sqlalchemy.orm import Session

from src.database import Point, get_sync_session
from src.logger import get_logger

logger = get_logger(__name__)


class PointRepo:
    @staticmethod
    def create_points(points: list[tuple[str, float, float]], session: Session | None = None) -> None:
        logger.info("Creating points")
        if not session:
            session = get_sync_session()
        points_db = [Point(name=name, latitude=x, longitude=y) for name, x, y in points]
        logger.debug("Points: {}".format(points_db))
        session.add_all(points_db)
        session.commit()
        logger.info("Points created")

    @staticmethod
    def get_point_by_id(point_id: int, session: Session | None = None) -> Point:
        if not session:
            session = get_sync_session()
        logger.info("Getting point with id {}".format(point_id))
        point = session.query(Point).filter(Point.id == point_id).first()
        logger.debug("Point: {}".format(point))
        if not point:
            raise ValueError(f"Point with id {point_id} not found")
        return point

    @staticmethod
    def get_points(session: Session | None = None) -> list[Point]:
        if not session:
            session = get_sync_session()
        logger.info("Getting all points")
        points = session.query(Point).all()
        logger.debug("Points: {}".format(points))
        return points
