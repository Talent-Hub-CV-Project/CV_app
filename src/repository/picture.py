from sqlalchemy.orm import Session

from src.database import Picture, get_sync_session


class PictureRepo:
    @staticmethod
    def get_picture(picture_id: int, session: Session | None = None) -> Picture:
        if not session:
            session = get_sync_session()
        pic = session.query(Picture).filter(Picture.id == picture_id).first()
        if not pic:
            raise ValueError(f"Picture with id {picture_id} not found")
        return pic
