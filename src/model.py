from logging import Logger

from PIL.Image import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results  # type: ignore[import-untyped]

from src.logger import get_logger


class Model:
    logger: Logger = get_logger(__name__)
    model: YOLO = YOLO("models/yolov8n.onnx")

    def __init__(self) -> None:
        pass

    def predict(self, image: Image) -> list[Results]:
        return self.model(image)  # type: ignore[no-any-return]
