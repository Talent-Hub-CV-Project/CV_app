from sqlalchemy.orm import Session

from src.database import ModelPredictionClass, get_sync_session


class ModelClassRepo:
    @staticmethod
    def create_classes(session: Session | None = None) -> None:
        if session is None:
            session = get_sync_session()
        # taken from yolo output
        classes = {
            0: "person",
            1: "bicycle",
            2: "car",
            3: "motorcycle",
            4: "airplane",
            5: "bus",
            6: "train",
            7: "truck",
            8: "boat",
            9: "traffic light",
            10: "fire hydrant",
            11: "stop sign",
            12: "parking meter",
            13: "bench",
            14: "bird",
            15: "cat",
            16: "dog",
            17: "horse",
            18: "sheep",
            19: "cow",
            20: "elephant",
            21: "bear",
            22: "zebra",
            23: "giraffe",
            24: "backpack",
            25: "umbrella",
            26: "handbag",
            27: "tie",
            28: "suitcase",
            29: "frisbee",
            30: "skis",
            31: "snowboard",
            32: "sports ball",
            33: "kite",
            34: "baseball bat",
            35: "baseball glove",
            36: "skateboard",
            37: "surfboard",
            38: "tennis racket",
            39: "bottle",
            40: "wine glass",
            41: "cup",
            42: "fork",
            43: "knife",
            44: "spoon",
            45: "bowl",
            46: "banana",
            47: "apple",
            48: "sandwich",
            49: "orange",
            50: "broccoli",
            51: "carrot",
            52: "hot dog",
            53: "pizza",
            54: "donut",
            55: "cake",
            56: "chair",
            57: "couch",
            58: "potted plant",
            59: "bed",
            60: "dining table",
            61: "toilet",
            62: "tv",
            63: "laptop",
            64: "mouse",
            65: "remote",
            66: "keyboard",
            67: "cell phone",
            68: "microwave",
            69: "oven",
            70: "toaster",
            71: "sink",
            72: "refrigerator",
            73: "book",
            74: "clock",
            75: "vase",
            76: "scissors",
            77: "teddy bear",
            78: "hair drier",
            79: "toothbrush",
        }
        classes_in_db = session.query(ModelPredictionClass).count()
        if classes_in_db != 0:
            return
        for class_id, class_name in classes.items():
            session.add(ModelPredictionClass(id=class_id, name=class_name))
        session.commit()

    @staticmethod
    def get_model_prediction_class(cls: int, session: Session | None = None) -> ModelPredictionClass:
        if session is None:
            session = get_sync_session()

        prediction_class = session.query(ModelPredictionClass).filter(ModelPredictionClass.id == cls).first()
        if prediction_class is None:
            raise ValueError(f"Prediction class with id {cls} not found")
        return prediction_class
