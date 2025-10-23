import unittest
from pathlib import Path
from yolo.model_registry import ModelRegistry, YoloModelVersion


class ModelRegistryTest(unittest.TestCase):
    def setUp(self):
        self.models_dir = Path("yolo/models")
        self.registry = ModelRegistry(self.models_dir)

    def test_get_model_path_returns_correct_path_for_v8n(self):
        model_path = self.registry.get_model_path(YoloModelVersion.V8N)
        
        expected_path = self.models_dir / "yolov8n.pt"
        self.assertEqual(model_path, expected_path)

    def test_get_model_path_returns_correct_path_for_v11x(self):
        model_path = self.registry.get_model_path(YoloModelVersion.V11X)

        expected_path = self.models_dir / "yolo11x.pt"
        self.assertEqual(model_path, expected_path)

    def test_get_model_path_returns_correct_path_for_segmentation_model(self):
        model_path = self.registry.get_model_path(YoloModelVersion.V11M_SEG)

        expected_path = self.models_dir / "yolo11m-seg.pt"
        self.assertEqual(model_path, expected_path)

    def test_get_model_path_returns_correct_path_for_pose_model(self):
        model_path = self.registry.get_model_path(YoloModelVersion.V8L_POSE)

        expected_path = self.models_dir / "yolov8l-pose.pt"
        self.assertEqual(model_path, expected_path)

    def test_get_model_path_returns_correct_path_for_classification_model(self):
        model_path = self.registry.get_model_path(YoloModelVersion.V11N_CLS)

        expected_path = self.models_dir / "yolo11n-cls.pt"
        self.assertEqual(model_path, expected_path)

    def test_get_model_path_returns_correct_path_for_obb_model(self):
        model_path = self.registry.get_model_path(YoloModelVersion.V8S_OBB)

        expected_path = self.models_dir / "yolov8s-obb.pt"
        self.assertEqual(model_path, expected_path)

    def test_ensure_models_directory_exists_creates_directory(self):
        test_dir = Path("test_models")
        test_registry = ModelRegistry(test_dir)
        
        test_registry.ensure_models_directory_exists()
        
        self.assertTrue(test_dir.exists())
        test_dir.rmdir()

    def test_all_model_versions_have_unique_filenames(self):
        filenames = set()
        for version in YoloModelVersion:
            filename = version.value
            self.assertNotIn(filename, filenames, f"Duplicate filename: {filename}")
            filenames.add(filename)


if __name__ == "__main__":
    unittest.main()

