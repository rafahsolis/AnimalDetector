from pathlib import Path
from typing import Dict
from enum import Enum


class YoloModelVersion(Enum):
    V8N = "yolov8n.pt"
    V8S = "yolov8s.pt"
    V8M = "yolov8m.pt"
    V8L = "yolov8l.pt"
    V8X = "yolov8x.pt"
    V11N = "yolo11n.pt"
    V11S = "yolo11s.pt"
    V11M = "yolo11m.pt"
    V11L = "yolo11l.pt"
    V11X = "yolo11x.pt"
    V8N_SEG = "yolov8n-seg.pt"
    V8S_SEG = "yolov8s-seg.pt"
    V8M_SEG = "yolov8m-seg.pt"
    V8L_SEG = "yolov8l-seg.pt"
    V8X_SEG = "yolov8x-seg.pt"
    V11N_SEG = "yolo11n-seg.pt"
    V11S_SEG = "yolo11s-seg.pt"
    V11M_SEG = "yolo11m-seg.pt"
    V11L_SEG = "yolo11l-seg.pt"
    V11X_SEG = "yolo11x-seg.pt"
    V8N_POSE = "yolov8n-pose.pt"
    V8S_POSE = "yolov8s-pose.pt"
    V8M_POSE = "yolov8m-pose.pt"
    V8L_POSE = "yolov8l-pose.pt"
    V8X_POSE = "yolov8x-pose.pt"
    V11N_POSE = "yolo11n-pose.pt"
    V11S_POSE = "yolo11s-pose.pt"
    V11M_POSE = "yolo11m-pose.pt"
    V11L_POSE = "yolo11l-pose.pt"
    V11X_POSE = "yolo11x-pose.pt"
    V8N_CLS = "yolov8n-cls.pt"
    V8S_CLS = "yolov8s-cls.pt"
    V8M_CLS = "yolov8m-cls.pt"
    V8L_CLS = "yolov8l-cls.pt"
    V8X_CLS = "yolov8x-cls.pt"
    V11N_CLS = "yolo11n-cls.pt"
    V11S_CLS = "yolo11s-cls.pt"
    V11M_CLS = "yolo11m-cls.pt"
    V11L_CLS = "yolo11l-cls.pt"
    V11X_CLS = "yolo11x-cls.pt"
    V8N_OBB = "yolov8n-obb.pt"
    V8S_OBB = "yolov8s-obb.pt"
    V8M_OBB = "yolov8m-obb.pt"
    V8L_OBB = "yolov8l-obb.pt"
    V8X_OBB = "yolov8x-obb.pt"
    V11N_OBB = "yolo11n-obb.pt"
    V11S_OBB = "yolo11s-obb.pt"
    V11M_OBB = "yolo11m-obb.pt"
    V11L_OBB = "yolo11l-obb.pt"
    V11X_OBB = "yolo11x-obb.pt"


class ModelRegistry:
    def __init__(self, models_dir: Path) -> None:
        self._models_dir = models_dir

    def get_model_path(self, version: YoloModelVersion) -> Path:
        model_path = self._models_dir / version.value
        return model_path

    def is_model_available(self, version: YoloModelVersion) -> bool:
        model_path = self.get_model_path(version)
        return model_path.exists()

    def get_all_available_models(self) -> Dict[str, Path]:
        available_models = {}
        for version in YoloModelVersion:
            if self.is_model_available(version):
                available_models[version.name] = self.get_model_path(version)
        return available_models

    def ensure_models_directory_exists(self) -> None:
        self._models_dir.mkdir(parents=True, exist_ok=True)

