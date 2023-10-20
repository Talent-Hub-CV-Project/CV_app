from logging import Logger

import numpy as np
import numpy.typing as npt
from PIL.Image import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results  # type: ignore[import-untyped]

from src.logger import get_logger


class Model:
    logger: Logger = get_logger(__name__)
    model: YOLO = YOLO("models/yolov8n.onnx", task="detect")

    def __init__(self) -> None:
        pass

    def predict(self, image: npt.NDArray[np.int_] | Image) -> list[Results]:
        return self.model(image)  # type: ignore[no-any-return]
