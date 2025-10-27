import unittest
from pathlib import Path
from unittest.mock import Mock
from image_server import (
    get_server_ip,
    get_server_port,
    create_server_address,
    assign_root_to_server,
    is_image_file,
    list_images,
    ImageRequestHandler,
    is_safe_child,
    is_child_of_parent
)

class TestServerConfiguration(unittest.TestCase):
    def test_get_server_ip_returns_default_when_none(self):
        result = get_server_ip(None)
        self.assertEqual(result, '127.0.0.1')

    def test_get_server_ip_returns_custom_ip(self):
        result = get_server_ip('0.0.0.0')
        self.assertEqual(result, '0.0.0.0')

    def test_get_server_port_returns_default_when_none(self):
        result = get_server_port(None)
        self.assertEqual(result, 8000)

    def test_get_server_port_returns_custom_port(self):
        result = get_server_port(8080)
        self.assertEqual(result, 8080)

class TestServerAddress(unittest.TestCase):
    def test_create_server_address_returns_tuple(self):
        address = create_server_address('127.0.0.1', 8000)
        self.assertEqual(address, ('127.0.0.1', 8000))

    def test_create_server_address_is_tuple_type(self):
        address = create_server_address('0.0.0.0', 9000)
        self.assertIsInstance(address, tuple)

class TestServerRoot(unittest.TestCase):
    def test_assign_root_to_server_sets_attribute(self):
        mock_server = Mock()
        root_path = Path('/tmp/images')
        assign_root_to_server(mock_server, root_path)
        self.assertEqual(mock_server.root, root_path)

class TestPathSafety(unittest.TestCase):
    def test_is_safe_child_returns_true_for_valid_child(self):
        parent = Path('/tmp/parent')
        child = Path('/tmp/parent/child')
        result = is_safe_child(parent, child)
        self.assertTrue(result)

    def test_is_safe_child_returns_false_for_path_traversal(self):
        parent = Path('/tmp/parent')
        child = Path('/tmp/other')
        result = is_safe_child(parent, child)
        self.assertFalse(result)

    def test_is_child_of_parent_returns_true_when_valid(self):
        parent = Path('/home/user/documents')
        child = Path('/home/user/documents/file.txt')
        result = is_child_of_parent(parent, child)
        self.assertTrue(result)

    def test_is_child_of_parent_returns_false_when_invalid(self):
        parent = Path('/home/user/documents')
        child = Path('/home/user/pictures/photo.jpg')
        result = is_child_of_parent(parent, child)
        self.assertFalse(result)

class TestImageFileDetection(unittest.TestCase):
    def test_is_image_file_returns_true_for_jpg(self):
        temp_dir = self.create_temp_directory()
        jpg_file = self.create_temp_file(temp_dir, "test.jpg")
        result = is_image_file(jpg_file)
        self.cleanup_temp_files(temp_dir)
        self.assertTrue(result)

    def test_is_image_file_returns_false_for_txt(self):
        temp_dir = self.create_temp_directory()
        txt_file = self.create_temp_file(temp_dir, "test.txt")
        result = is_image_file(txt_file)
        self.cleanup_temp_files(temp_dir)
        self.assertFalse(result)

    @staticmethod
    def create_temp_directory() -> Path:
        temp_dir = Path("test_images")
        temp_dir.mkdir(exist_ok=True)
        return temp_dir

    @staticmethod
    def create_temp_file(directory: Path, filename: str) -> Path:
        file_path = directory / filename
        file_path.touch()
        return file_path

    @staticmethod
    def cleanup_temp_files(directory: Path) -> None:
        for file in directory.iterdir():
            file.unlink()
        directory.rmdir()

class TestListImages(unittest.TestCase):
    def test_list_images_returns_only_image_files(self):
        temp_dir = Path("test_images")
        temp_dir.mkdir(exist_ok=True)
        (temp_dir / "a.jpg").touch()
        (temp_dir / "b.txt").touch()
        images = list_images(temp_dir)
        self.assertIn("a.jpg", images)
        self.assertNotIn("b.txt", images)
        self.cleanup_directory(temp_dir)

    @staticmethod
    def cleanup_directory(directory: Path) -> None:
        for file in directory.iterdir():
            file.unlink()
        directory.rmdir()

class TestImageRequestHandler(unittest.TestCase):
    def test_get_server_root_returns_server_root_attribute(self):
        handler = self.create_mock_handler()
        mock_server = Mock()
        expected_root = Path('/tmp/test')
        mock_server.root = expected_root
        handler.server = mock_server
        result = handler.get_server_root()
        self.assertEqual(result, expected_root)

    @staticmethod
    def create_mock_handler() -> ImageRequestHandler:
        mock_request = Mock()
        mock_address = ('127.0.0.1', 8000)
        mock_server = Mock()
        return ImageRequestHandler(mock_request, mock_address, mock_server)

if __name__ == "__main__":
    unittest.main()
