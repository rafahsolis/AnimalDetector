import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from yolo.yolo import ModelTrainer


class ModelTrainerTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.dataset_path = Path(self.temp_dir.name)
        self.model_arch = "yolov8n.yaml"
        self.device = "cpu"
        self.trainer = ModelTrainer(self.dataset_path, self.model_arch, self.device)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_init_sets_dataset_path(self):
        self.assertEqual(self.trainer.dataset_path, self.dataset_path)

    def test_init_sets_model_architecture(self):
        self.assertEqual(self.trainer.model_arch, self.model_arch)

    def test_init_sets_device(self):
        self.assertEqual(self.trainer.device, self.device)

    def test_get_data_yaml_path_returns_correct_path(self):
        expected = self.dataset_path / "data.yaml"
        result = self.trainer._get_data_yaml_path()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
import unittest
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from yolo.yolo import ImageLoader


class ImageLoaderTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.image_dir = Path(self.temp_dir.name)
        self.loader = ImageLoader(self.image_dir)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_load_images_returns_empty_list_when_no_images(self):
        images = self.loader.load_images()
        self.assertEqual(images, [])

    def test_load_images_finds_jpg_files(self):
        self.create_test_file("test1.jpg")
        images = self.loader.load_images()
        self.assertEqual(len(images), 1)

    def test_load_images_finds_png_files(self):
        self.create_test_file("test2.png")
        images = self.loader.load_images()
        self.assertEqual(len(images), 1)

    def test_load_images_finds_jpeg_files(self):
        self.create_test_file("test3.jpeg")
        images = self.loader.load_images()
        self.assertEqual(len(images), 1)

    def test_load_images_ignores_unsupported_extensions(self):
        self.create_test_file("test.txt")
        self.create_test_file("test.pdf")
        images = self.loader.load_images()
        self.assertEqual(len(images), 0)

    def test_load_images_finds_multiple_images(self):
        self.create_test_file("img1.jpg")
        self.create_test_file("img2.png")
        self.create_test_file("img3.jpeg")
        images = self.loader.load_images()
        self.assertEqual(len(images), 3)

    def test_load_images_case_insensitive_extensions(self):
        self.create_test_file("test.JPG")
        self.create_test_file("test2.PNG")
        images = self.loader.load_images()
        self.assertEqual(len(images), 2)

    def create_test_file(self, filename: str) -> None:
        file_path = self.image_dir / filename
        file_path.touch()


if __name__ == "__main__":
    unittest.main()

