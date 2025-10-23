import unittest
import os
os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

from unittest.mock import Mock, patch
from pathlib import Path
from tempfile import TemporaryDirectory
from yolo.yolo import AnimalDetectionPipeline, ImageLoader, AnimalDetector, ResultLogger


class AnimalDetectionPipelineTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.image_dir = Path(self.temp_dir.name)
        self.log_path = Path(self.temp_dir.name) / "test.csv"
        
        self.loader = ImageLoader(self.image_dir)
        self.detector = Mock(spec=AnimalDetector)
        self.logger = ResultLogger(self.log_path)
        
        self.pipeline = AnimalDetectionPipeline(self.loader, self.detector, self.logger)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_sets_loader(self):
        self.assertEqual(self.pipeline.loader, self.loader)

    def test_init_sets_detector(self):
        self.assertEqual(self.pipeline.detector, self.detector)

    def test_init_sets_logger(self):
        self.assertEqual(self.pipeline.logger, self.logger)

    def test_run_processes_all_images(self):
        self.create_test_images(3)
        self.detector.detect.return_value = []
        self.pipeline.run()
        self.assertEqual(self.detector.detect.call_count, 3)

    def test_run_with_no_images(self):
        self.detector.detect.return_value = []
        self.pipeline.run()
        self.assertEqual(self.detector.detect.call_count, 0)

    def test_process_single_image_calls_detector(self):
        image_path = self.create_test_image("test.jpg")
        self.detector.detect.return_value = []
        self.pipeline._process_single_image(image_path)
        self.detector.detect.assert_called_once_with(image_path)

    def test_process_single_image_logs_detections(self):
        image_path = self.create_test_image("test.jpg")
        detections = self.create_test_detections()
        self.detector.detect.return_value = detections
        self.pipeline._process_single_image(image_path)
        log_content = self.log_path.read_text()
        self.assertIn("test.jpg", log_content)

    def test_process_images_iterates_all(self):
        images = [self.create_test_image(f"img{i}.jpg") for i in range(3)]
        self.detector.detect.return_value = []
        self.pipeline._process_images(images)
        self.assertEqual(self.detector.detect.call_count, 3)

    def create_test_images(self, count: int) -> None:
        for i in range(count):
            self.create_test_image(f"test{i}.jpg")

    def create_test_image(self, filename: str) -> Path:
        image_path = self.image_dir / filename
        image_path.touch()
        return image_path

    def create_test_detections(self) -> list:
        return [{
            "class_id": 0,
            "class_name": "cat",
            "confidence": 0.95,
            "bbox": [100, 200, 300, 400]
        }]


if __name__ == "__main__":
    unittest.main()

