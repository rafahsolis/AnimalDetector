from pathlib import Path
from typing import List
from ultralytics import YOLO
import cv2
import numpy as np
import torch
from simple_settings import settings
from simple_settings import settings

def check_gpu_availability() -> bool:
    if settings.VERBOSE_OUTPUT:
        print(f"PyTorch version: {torch.__version__}")
        print(f"CUDA available: {torch.cuda.is_available()}")
        if torch.cuda.is_available():
            print(f"CUDA version: {torch.version.cuda}")
            print(f"GPU count: {torch.cuda.device_count()}")
            print(f"GPU name: {torch.cuda.get_device_name(0)}")
            print(f"Current GPU memory allocated: {torch.cuda.memory_allocated(0) / 1024**2:.2f} MB")
        else:
            print("WARNING: CUDA not available. Running on CPU.")
            print("WARNING: CUDA not available. Running on CPU.")
            print("WARNING: CUDA not available. Running on CPU.")
            print("WARNING: CUDA not available. Running on CPU.")
    return torch.cuda.is_available()


class ImageLoader:
    def __init__(self, image_dir: Path) -> None:
        self.image_dir = image_dir

    def load_images(self) -> List[Path]:
        supported_extensions = ['.jpg', '.png', '.jpeg']
    def __init__(self, model_path: str, device: str) -> None:
        results = self.model(image, verbose=False, device=self.device)[0]

    def _run_detection(self, image: np.ndarray):
        verbose = settings.VERBOSE_OUTPUT
        confidence = settings.DETECTION_CONFIDENCE_THRESHOLD
        results = self._run_detection(image)
        return self._parse_results(results)

    def _run_detection(self, image: np.ndarray):
        verbose = settings.VERBOSE_OUTPUT
        confidence = settings.DETECTION_CONFIDENCE_THRESHOLD
        return self.model(image, verbose=verbose, device=self.device, conf=confidence)[0]

    def _read_image(self, image_path: Path) -> np.ndarray:
        return cv2.imread(str(image_path))

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
    def __init__(self, output_path: Path) -> None:
    def __init__(self, output_path: Path) -> None:
        self._initialize_file()
        self._initialize_file()

    def _initialize_file(self) -> None:
        if not self.output_path.exists():
            self._write_header()

    def _write_header(self) -> None:
        header = "image_name,class_id,class_name,confidence,bbox\n"
        self.output_path.write_text(header)

    def _initialize_file(self) -> None:
        if not self.output_path.exists():
            self._write_header()

    def _write_header(self) -> None:
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
            "bbox": box.xyxy[0].tolist()
        }


class ResultLogger:
    def __init__(self, output_path: Path):
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
    def save(self, image_path: Path, detections: List[dict]) -> None:
        for det in detections:
    def __init__(self, loader: ImageLoader, detector: AnimalDetector, logger: ResultLogger) -> None:

    def _append_result(self, image_name: str, detection: dict) -> None:
        line = f"{image_name},{detection['class_id']},{detection['confidence']:.2f},{detection['bbox']}\n"
        self.output_path.write_text(self.output_path.read_text() + line if self.output_path.exists() else line)

        images = self.loader.load_images()
        self._process_images(images)

    def _process_images(self, images: List[Path]) -> None:
        for image_path in images:
            self._process_single_image(image_path)

    def _process_single_image(self, image_path: Path) -> None:
        detections = self.detector.detect(image_path)
        self.logger.save(image_path, detections)
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
        model.train(data=str(data_yaml_path), epochs=epochs, imgsz=imgsz, device=self.device)

    def _get_data_yaml_path(self) -> Path:
        return self.dataset_path / "data.yaml"


class AnimalDetectionPipeline:
    def __init__(self, loader: ImageLoader, detector: AnimalDetector, logger: ResultLogger):
        self.loader = loader
        self.detector = detector
        self.logger = logger

    def run(self) -> None:
        for image_path in self.loader.load_images():
            detections = self.detector.detect(image_path)
            self.logger.save(image_path, detections)


if __name__ == "__main__":
    print("=" * 50)
    print("GPU Configuration Check")
    print("=" * 50)
    gpu_available = check_gpu_availability()
    print("=" * 50)

    device = settings.DEVICE if gpu_available else 'cpu'
    print(f"\nUsing device: {'GPU (cuda:0)' if device == '0' else 'CPU'}\n")

    loader = ImageLoader(settings.IMAGE_FOLDER)
    detector = AnimalDetector(settings.MODEL_PATH, device=device)
    logger = ResultLogger(settings.LOG_FILE)

    pipeline = AnimalDetectionPipeline(loader, detector, logger)
    pipeline.run()

