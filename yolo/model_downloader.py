from pathlib import Path
from ultralytics import YOLO
from ultralytics.utils import SETTINGS
import logging
import shutil

logger = logging.getLogger(__name__)


class ModelDownloader:
    def __init__(self, models_dir: Path) -> None:
        self._models_dir = models_dir

    def download_model(self, model_name: str) -> Path:
        self._ensure_models_directory_exists()
        model_path = self._get_model_path(model_name)
        
        if self._is_model_already_downloaded(model_path):
            logger.info(f"Model {model_name} already exists at {model_path}")
            return model_path
        
        self._download_and_save_model(model_name, model_path)
        return model_path

    def _ensure_models_directory_exists(self) -> None:
        self._models_dir.mkdir(parents=True, exist_ok=True)

    def _get_model_path(self, model_name: str) -> Path:
        return self._models_dir / model_name

    def _is_model_already_downloaded(self, model_path: Path) -> bool:
        return model_path.exists()

    def _download_and_save_model(self, model_name: str, model_path: Path) -> None:
        logger.info(f"Downloading model {model_name}...")

        temp_model = YOLO(model_name)
        source_path = self._find_downloaded_model(model_name)
        self._move_model_to_destination(source_path, model_path)

        logger.info(f"Model {model_name} saved to {model_path}")

    def _find_downloaded_model(self, model_name: str) -> Path:
        current_dir_path = Path.cwd() / model_name
        if current_dir_path.exists():
            return current_dir_path

        cache_path = self._get_ultralytics_cache_path(model_name)
        if cache_path.exists():
            return cache_path

        raise FileNotFoundError(f"Could not find downloaded model {model_name}")

    def _get_ultralytics_cache_path(self, model_name: str) -> Path:
        weights_dir = Path(SETTINGS['weights_dir'])
        return weights_dir / model_name

    def _move_model_to_destination(self, source_path: Path, destination_path: Path) -> None:
        if source_path.exists():
            shutil.move(str(source_path), str(destination_path))
            logger.info(f"Moved model from {source_path} to {destination_path}")
        else:
            raise FileNotFoundError(f"Source model not found at {source_path}")

    def download_all_standard_models(self) -> None:
        models = ['yolov8n.pt', 'yolov8s.pt', 'yolov8m.pt', 'yolov8l.pt', 'yolov8x.pt',
                  'yolo11n.pt', 'yolo11s.pt', 'yolo11m.pt', 'yolo11l.pt', 'yolo11x.pt']
        for model_name in models:
            self.download_model(model_name)

    def download_all_detection_models(self) -> None:
        self.download_all_standard_models()

    def download_all_segmentation_models(self) -> None:
        models = ['yolov8n-seg.pt', 'yolov8s-seg.pt', 'yolov8m-seg.pt', 'yolov8l-seg.pt', 'yolov8x-seg.pt',
                  'yolo11n-seg.pt', 'yolo11s-seg.pt', 'yolo11m-seg.pt', 'yolo11l-seg.pt', 'yolo11x-seg.pt']
        for model_name in models:
            self.download_model(model_name)

    def download_all_pose_models(self) -> None:
        models = ['yolov8n-pose.pt', 'yolov8s-pose.pt', 'yolov8m-pose.pt', 'yolov8l-pose.pt', 'yolov8x-pose.pt',
                  'yolo11n-pose.pt', 'yolo11s-pose.pt', 'yolo11m-pose.pt', 'yolo11l-pose.pt', 'yolo11x-pose.pt']
        for model_name in models:
            self.download_model(model_name)

    def download_all_classification_models(self) -> None:
        models = ['yolov8n-cls.pt', 'yolov8s-cls.pt', 'yolov8m-cls.pt', 'yolov8l-cls.pt', 'yolov8x-cls.pt',
                  'yolo11n-cls.pt', 'yolo11s-cls.pt', 'yolo11m-cls.pt', 'yolo11l-cls.pt', 'yolo11x-cls.pt']
        for model_name in models:
            self.download_model(model_name)

    def download_all_obb_models(self) -> None:
        models = ['yolov8n-obb.pt', 'yolov8s-obb.pt', 'yolov8m-obb.pt', 'yolov8l-obb.pt', 'yolov8x-obb.pt',
                  'yolo11n-obb.pt', 'yolo11s-obb.pt', 'yolo11m-obb.pt', 'yolo11l-obb.pt', 'yolo11x-obb.pt']
        for model_name in models:
            self.download_model(model_name)

    def download_all_available_models(self) -> None:
        self.download_all_detection_models()
        self.download_all_segmentation_models()
        self.download_all_pose_models()
        self.download_all_classification_models()
        self.download_all_obb_models()


