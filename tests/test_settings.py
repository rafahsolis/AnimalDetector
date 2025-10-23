import unittest
import os
os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

from pathlib import Path
from simple_settings import settings


class SettingsTest(unittest.TestCase):
    def test_device_setting_is_defined(self):
        self.assertIsNotNone(settings.DEVICE)

    def test_model_path_setting_is_defined(self):
        self.assertIsNotNone(settings.MODEL_PATH)

    def test_image_folder_setting_is_path(self):
        self.assertIsInstance(settings.IMAGE_FOLDER, Path)

    def test_log_file_setting_is_path(self):
        self.assertIsInstance(settings.LOG_FILE, Path)

    def test_confidence_threshold_is_float(self):
        self.assertIsInstance(settings.DETECTION_CONFIDENCE_THRESHOLD, float)

    def test_confidence_threshold_is_valid_range(self):
        threshold = settings.DETECTION_CONFIDENCE_THRESHOLD
        self.assertGreaterEqual(threshold, 0.0)
        self.assertLessEqual(threshold, 1.0)

    def test_verbose_output_is_boolean(self):
        self.assertIsInstance(settings.VERBOSE_OUTPUT, bool)

    def test_target_animals_is_list(self):
        self.assertIsInstance(settings.TARGET_ANIMALS, list)

    def test_target_animals_contains_expected_species(self):
        expected_animals = ["rabbit", "fox", "wild_boar", "bird"]
        for animal in expected_animals:
            self.assertIn(animal, settings.TARGET_ANIMALS)


if __name__ == "__main__":
    unittest.main()

