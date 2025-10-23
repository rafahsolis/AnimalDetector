import unittest
import os
os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

from unittest.mock import patch, Mock
import torch
from yolo.yolo import check_gpu_availability, _print_cuda_warning


class CudaWarningTest(unittest.TestCase):
    @patch('yolo.yolo.torch.cuda.is_available')
    @patch('yolo.yolo.settings')
    @patch('builtins.print')
    def test_prints_warning_when_cuda_unavailable(self, mock_print, mock_settings, mock_cuda):
        mock_cuda.return_value = False
        mock_settings.VERBOSE_OUTPUT = True
        
        check_gpu_availability()
        
        warning_printed = self.check_warning_was_printed(mock_print)
        self.assertTrue(warning_printed)

    @patch('builtins.print')
    def test_print_cuda_warning_outputs_message(self, mock_print):
        _print_cuda_warning()
        
        mock_print.assert_called_once()
        call_args = mock_print.call_args[0][0]
        self.assertIn("WARNING", call_args)
        self.assertIn("CUDA", call_args)

    def check_warning_was_printed(self, mock_print) -> bool:
        for call in mock_print.call_args_list:
            if "WARNING" in str(call):
                return True
        return False


if __name__ == "__main__":
    unittest.main()
import unittest
import os
os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
import numpy as np
from yolo.yolo import AnimalDetector


class AnimalDetectorTest(unittest.TestCase):
    def setUp(self):
        self.model_path = "yolov8n.pt"
        self.device = "cpu"
        self.mock_model = self.create_mock_model()

    def create_mock_model(self) -> Mock:
        mock = Mock()
        mock.return_value = [self.create_mock_results()]
        return mock

    def create_mock_results(self) -> Mock:
        results = Mock()
        results.boxes = self.create_mock_boxes()
        results.names = {0: "cat", 1: "dog"}
        return results

    def create_mock_boxes(self) -> Mock:
        boxes = Mock()
        boxes.conf = [0.95]
        boxes.cls = [0]
        box = Mock()
        box.xyxy = [Mock(tolist=lambda: [100, 200, 300, 400])]
        boxes.__iter__ = lambda self: iter([box])
        return boxes

    @patch('yolo.yolo.YOLO')
    def test_init_creates_model(self, mock_yolo):
        detector = AnimalDetector(self.model_path, self.device)
        mock_yolo.assert_called_once_with(self.model_path)

    @patch('yolo.yolo.YOLO')
    def test_init_sets_device(self, mock_yolo):
        detector = AnimalDetector(self.model_path, self.device)
        self.assertEqual(detector.device, self.device)

    @patch('yolo.yolo.cv2.imread')
    @patch('yolo.yolo.YOLO')
    def test_read_image_returns_numpy_array(self, mock_yolo, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3))
        detector = AnimalDetector(self.model_path, self.device)
        image_path = Path("test.jpg")
        result = detector._read_image(image_path)
        self.assertIsInstance(result, np.ndarray)

    @patch('yolo.yolo.cv2.imread')
    @patch('yolo.yolo.YOLO')
    def test_read_image_calls_imread_with_string_path(self, mock_yolo, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3))
        detector = AnimalDetector(self.model_path, self.device)
        image_path = Path("test.jpg")
        detector._read_image(image_path)
        mock_imread.assert_called_once_with(str(image_path))

    @patch('yolo.yolo.cv2.imread')
    @patch('yolo.yolo.YOLO')
    def test_detect_returns_list_of_dicts(self, mock_yolo, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3))
        mock_yolo.return_value = self.mock_model
        detector = AnimalDetector(self.model_path, self.device)
        detections = detector.detect(Path("test.jpg"))
        self.assertIsInstance(detections, list)

    @patch('yolo.yolo.cv2.imread')
    @patch('yolo.yolo.YOLO')
    def test_detect_returns_detection_with_class_id(self, mock_yolo, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3))
        mock_yolo.return_value = self.mock_model
        detector = AnimalDetector(self.model_path, self.device)
        detections = detector.detect(Path("test.jpg"))
        self.assertIn('class_id', detections[0])

    @patch('yolo.yolo.cv2.imread')
    @patch('yolo.yolo.YOLO')
    def test_detect_returns_detection_with_class_name(self, mock_yolo, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3))
        mock_yolo.return_value = self.mock_model
        detector = AnimalDetector(self.model_path, self.device)
        detections = detector.detect(Path("test.jpg"))
        self.assertIn('class_name', detections[0])

    @patch('yolo.yolo.cv2.imread')
    @patch('yolo.yolo.YOLO')
    def test_detect_returns_detection_with_confidence(self, mock_yolo, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3))
        mock_yolo.return_value = self.mock_model
        detector = AnimalDetector(self.model_path, self.device)
        detections = detector.detect(Path("test.jpg"))
        self.assertIn('confidence', detections[0])

    @patch('yolo.yolo.cv2.imread')
    @patch('yolo.yolo.YOLO')
    def test_detect_returns_detection_with_bbox(self, mock_yolo, mock_imread):
        mock_imread.return_value = np.zeros((100, 100, 3))
        mock_yolo.return_value = self.mock_model
        detector = AnimalDetector(self.model_path, self.device)
        detections = detector.detect(Path("test.jpg"))
        self.assertIn('bbox', detections[0])

    def test_create_detection_dict_creates_correct_structure(self):
        box = Mock()
        box.xyxy = [Mock(tolist=lambda: [1, 2, 3, 4])]
        conf = 0.85
        cls = 1
        results = Mock()
        results.names = {1: "dog"}
        
        detection = AnimalDetector._create_detection_dict(box, conf, cls, results)
        
        self.assertEqual(detection['class_id'], 1)
        self.assertEqual(detection['class_name'], "dog")
        self.assertEqual(detection['confidence'], 0.85)
        self.assertEqual(detection['bbox'], [1, 2, 3, 4])


if __name__ == "__main__":
    unittest.main()

