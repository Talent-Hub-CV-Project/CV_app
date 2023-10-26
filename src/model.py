from logging import Logger

import numpy as np
import numpy.typing as npt
from PIL.Image import Image
from ultralytics import YOLO
from ultralytics.engine.results import Results  # type: ignore[import-untyped]

from src.logger import get_logger


class Model:
    logger: Logger = get_logger(__name__)

    def __init__(self, model_path: str = "models/yolov8n.onnx") -> None:
        self.model = YOLO(model_path, task="detect")

    def predict(self, image: npt.NDArray[np.int_] | Image) -> list[Results]:
        return self.model(image)  # type: ignore[no-any-return]
