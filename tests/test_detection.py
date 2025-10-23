import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from yolo.detection import AnimalDetector


class AnimalDetectorTest(unittest.TestCase):
    def setUp(self):
        self.model_path = Path("yolo/models/yolov8n.pt")
        self.device = "0"
        self.confidence_threshold = 0.25
        self.detector = AnimalDetector(self.model_path, self.device, self.confidence_threshold)

    @patch('yolo.detection.YOLO')
    def test_load_model_initializes_yolo_model(self, mock_yolo):
        self.detector.load_model()
        
        mock_yolo.assert_called_once_with(str(self.model_path))

    @patch('yolo.detection.YOLO')
    def test_detect_animals_in_image_returns_filtered_detections(self, mock_yolo):
        mock_model = self._create_mock_model()
        mock_yolo.return_value = mock_model
        
        image_path = Path("test_image.jpg")
        target_animals = ["rabbit", "fox"]
        
        detections = self.detector.detect_animals_in_image(image_path, target_animals)
        
        self.assertEqual(len(detections), 1)

    def _create_mock_model(self):
        mock_model = MagicMock()
        mock_result = self._create_mock_result()
        mock_model.predict.return_value = [mock_result]
        return mock_model

    def _create_mock_result(self):
        mock_result = Mock()
        mock_box = self._create_mock_box()
        mock_result.boxes = [mock_box]
        mock_result.names = {0: "rabbit"}
        return mock_result

    def _create_mock_box(self):
        mock_box = Mock()
        mock_box.cls = [0]
        mock_box.conf = [0.85]
        mock_box.xyxy = [[100, 100, 200, 200]]
        return mock_box


if __name__ == "__main__":
    unittest.main()

