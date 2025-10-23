import unittest
import os
os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

import torch
from yolo.yolo import check_gpu_availability


class GpuAvailabilityTest(unittest.TestCase):
    def test_check_gpu_availability_returns_boolean(self):
        result = check_gpu_availability()
        self.assertIsInstance(result, bool)

    def test_check_gpu_availability_matches_torch(self):
        result = check_gpu_availability()
        expected = torch.cuda.is_available()
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

