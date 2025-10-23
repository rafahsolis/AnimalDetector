import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from yolo.yolo import ResultLogger


class ResultLoggerTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.log_path = Path(self.temp_dir.name) / "test.csv"
        self.logger = ResultLogger(self.log_path)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initialize_creates_file_with_header(self):
        self.assertTrue(self.log_path.exists())

    def test_header_contains_required_columns(self):
        content = self.log_path.read_text()
        expected = "image_name,class_id,class_name,confidence,bbox\n"
        self.assertEqual(content, expected)

    def test_save_appends_detection_to_file(self):
        detection = self.create_test_detection()
        image_path = Path("test_image.jpg")
        self.logger.save(image_path, [detection])
        lines = self.read_log_lines()
        self.assertEqual(len(lines), 2)

    def test_save_writes_correct_format(self):
        detection = self.create_test_detection()
        image_path = Path("test_image.jpg")
        self.logger.save(image_path, [detection])
        lines = self.read_log_lines()
        self.assertIn("test_image.jpg", lines[1])

    def test_save_writes_class_id_correctly(self):
        detection = self.create_test_detection()
        image_path = Path("test.jpg")
        self.logger.save(image_path, [detection])
        lines = self.read_log_lines()
        self.assertIn("15", lines[1])

    def test_save_writes_class_name_correctly(self):
        detection = self.create_test_detection()
        image_path = Path("test.jpg")
        self.logger.save(image_path, [detection])
        lines = self.read_log_lines()
        self.assertIn("cat", lines[1])

    def test_save_handles_multiple_detections(self):
        detections = [self.create_test_detection(), self.create_test_detection()]
        image_path = Path("test.jpg")
        self.logger.save(image_path, detections)
        lines = self.read_log_lines()
        self.assertEqual(len(lines), 3)

    def test_format_detection_line_formats_confidence_correctly(self):
        detection = {"class_id": 1, "class_name": "dog", "confidence": 0.95123, "bbox": [1, 2, 3, 4]}
        line = self.logger._format_detection_line("test.jpg", detection)
        self.assertIn("0.95", line)

    def create_test_detection(self) -> dict:
        return {
            "class_id": 15,
            "class_name": "cat",
            "confidence": 0.95,
            "bbox": [100, 200, 300, 400]
        }

    def read_log_lines(self) -> list:
        return self.log_path.read_text().strip().split('\n')


if __name__ == "__main__":
    unittest.main()

