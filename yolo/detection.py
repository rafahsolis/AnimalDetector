from pathlib import Path
from typing import List, Dict, Any
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)


class AnimalDetector:
    def __init__(self, model_path: Path, device: str, confidence_threshold: float) -> None:
        self._model_path = model_path
        self._device = device
        self._confidence_threshold = confidence_threshold
        self._model = None

    def load_model(self) -> None:
        logger.info(f"Loading YOLO model from {self._model_path}")
        self._model = YOLO(str(self._model_path))

    def detect_animals_in_image(self, image_path: Path, target_animals: List[str]) -> List[Dict[str, Any]]:
        if self._model is None:
            self.load_model()
        
        results = self._run_prediction(image_path)
        detections = self._extract_detections(results, target_animals)
        return detections

    def _run_prediction(self, image_path: Path) -> Any:
        logger.debug(f"Running detection on {image_path}")
        return self._model.predict(
            source=str(image_path),
            conf=self._confidence_threshold,
            device=self._device,
            verbose=False
        )

    def _extract_detections(self, results: Any, target_animals: List[str]) -> List[Dict[str, Any]]:
        detections = []
        for result in results:
            filtered = self._filter_target_animals(result, target_animals)
            detections.extend(filtered)
        return detections

    def _filter_target_animals(self, result: Any, target_animals: List[str]) -> List[Dict[str, Any]]:
        detections = []
        for box in result.boxes:
            detection = self._create_detection_dict(box, result)
            if self._is_target_animal(detection, target_animals):
                detections.append(detection)
        return detections

    def _create_detection_dict(self, box: Any, result: Any) -> Dict[str, Any]:
        class_id = int(box.cls[0])
        return {
            'class_name': result.names[class_id],
            'confidence': float(box.conf[0]),
            'bbox': box.xyxy[0].tolist()
        }

    def _is_target_animal(self, detection: Dict[str, Any], target_animals: List[str]) -> bool:
        return detection['class_name'] in target_animals

