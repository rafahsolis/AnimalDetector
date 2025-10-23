from pathlib import Path
import logging.config
from settings import LOGGING, MODEL_PATH, IMAGE_FOLDER, DEVICE, DETECTION_CONFIDENCE_THRESHOLD, TARGET_ANIMALS
from yolo import AnimalDetector

logging.config.dictConfig(LOGGING)
logger = logging.getLogger('main')


class ImageProcessor:
    def __init__(self, detector: AnimalDetector, image_folder: Path) -> None:
        self._detector = detector
        self._image_folder = image_folder

    def process_all_images(self) -> None:
        image_paths = self._get_all_image_paths()
        for image_path in image_paths:
            self._process_single_image(image_path)

    def _get_all_image_paths(self) -> list[Path]:
        return list(self._image_folder.glob("*.jpg")) + list(self._image_folder.glob("*.png"))

    def _process_single_image(self, image_path: Path) -> None:
        logger.info(f"Processing image: {image_path}")
        detections = self._detector.detect_animals_in_image(image_path, TARGET_ANIMALS)
        self._log_detections(image_path, detections)

    def _log_detections(self, image_path: Path, detections: list) -> None:
        if detections:
            logger.info(f"Found {len(detections)} animals in {image_path.name}")
            for detection in detections:
                self._log_single_detection(detection)
        else:
            logger.info(f"No target animals found in {image_path.name}")

    def _log_single_detection(self, detection: dict) -> None:
        logger.info(f"  - {detection['class_name']}: {detection['confidence']:.2f}")


def create_detector() -> AnimalDetector:
    detector = AnimalDetector(MODEL_PATH, DEVICE, DETECTION_CONFIDENCE_THRESHOLD)
    detector.load_model()
    return detector


def main() -> None:
    logger.info("Starting Animal Detector")

    detector = create_detector()
    processor = ImageProcessor(detector, IMAGE_FOLDER)
    processor.process_all_images()

    logger.info("Processing complete")


if __name__ == "__main__":
    main()

