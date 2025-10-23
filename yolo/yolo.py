from pathlib import Path
from typing import List
import cv2
import numpy as np
from ultralytics import YOLO
from simple_settings import settings
from logger.config import get_logger

logger = get_logger('yolo')



class ImageLoader:
    def __init__(self, image_dir: Path) -> None:
        self.image_dir = image_dir

    def load_images(self) -> List[Path]:
        supported_extensions = ['.jpg', '.png', '.jpeg']
        images = self._filter_by_extension(supported_extensions)
        return images

    def _filter_by_extension(self, extensions: List[str]) -> List[Path]:
        return [f for f in self.image_dir.iterdir() if f.suffix.lower() in extensions]


class AnimalDetector:
    def __init__(self, model_path: str, device: str) -> None:
        self.model = YOLO(model_path)
        self.device = device

    def detect(self, image_path: Path) -> List[dict]:
        image = self._read_image(image_path)
        results = self._run_detection(image)
        return self._parse_results(results)

    def _read_image(self, image_path: Path) -> np.ndarray:
        return cv2.imread(str(image_path))

    def _run_detection(self, image: np.ndarray):
        verbose = settings.VERBOSE_OUTPUT
        confidence = settings.DETECTION_CONFIDENCE_THRESHOLD
        return self.model(image, verbose=verbose, device=self.device, conf=confidence)[0]

    def _parse_results(self, results) -> List[dict]:
        detections = []
        for box, conf, cls in zip(results.boxes, results.boxes.conf, results.boxes.cls):
            detection = self._create_detection_dict(box, conf, cls, results)
            detections.append(detection)
        return detections

    @staticmethod
    def _create_detection_dict(box, conf, cls, results) -> dict:
        class_id = int(cls)
        class_name = results.names[class_id]
        return {
            "class_id": class_id,
            "class_name": class_name,
            "confidence": float(conf),
            "bbox": box.xyxy[0].tolist()
        }


class ResultLogger:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self._initialize_file()

    def _initialize_file(self) -> None:
        if not self.output_path.exists():
            self._write_header()

    def _write_header(self) -> None:
        header = "image_name,class_id,class_name,confidence,bbox\n"
        self.output_path.write_text(header)

    def save(self, image_path: Path, detections: List[dict]) -> None:
        for det in detections:
            self._append_result(image_path.name, det)

    def _append_result(self, image_name: str, detection: dict) -> None:
        line = self._format_detection_line(image_name, detection)
        self._append_line(line)

    def _format_detection_line(self, image_name: str, detection: dict) -> str:
        class_id = detection['class_id']
        class_name = detection['class_name']
        confidence = detection['confidence']
        bbox = detection['bbox']
        return f"{image_name},{class_id},{class_name},{confidence:.2f},{bbox}\n"

    def _append_line(self, line: str) -> None:
        with open(self.output_path, 'a') as f:
            f.write(line)


class ModelTrainer:
    def __init__(self, dataset_path: Path, model_arch: str, device: str) -> None:
        self.dataset_path = dataset_path
        self.model_arch = model_arch
        self.device = device

    def train(self, epochs: int, imgsz: int) -> None:
        model = self._create_model()
        self._run_training(model, epochs, imgsz)

    def _create_model(self) -> YOLO:
        return YOLO(self.model_arch)

    def _run_training(self, model: YOLO, epochs: int, imgsz: int) -> None:
        data_yaml_path = self._get_data_yaml_path()
        self._train_model(model, data_yaml_path, epochs, imgsz)

    def _get_data_yaml_path(self) -> Path:
        return self.dataset_path / "data.yaml"

    def _train_model(self, model: YOLO, data_path: Path, epochs: int, imgsz: int) -> None:
        model.train(data=str(data_path), epochs=epochs, imgsz=imgsz, device=self.device)


class AnimalDetectionPipeline:
    def __init__(self, loader: ImageLoader, detector: AnimalDetector, result_logger: ResultLogger) -> None:
        self.loader = loader
        self.detector = detector
        self.logger = result_logger
        self.result_logger = result_logger

    def run(self) -> None:
        images = self.loader.load_images()
        self._process_images(images)

    def _process_images(self, images: List[Path]) -> None:
        for image_path in images:
            self._process_single_image(image_path)

    def _process_single_image(self, image_path: Path) -> None:
        detections = self.detector.detect(image_path)
        self.result_logger.save(image_path, detections)


