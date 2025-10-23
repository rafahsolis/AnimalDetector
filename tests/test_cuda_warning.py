import unittest
import os
os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

from unittest.mock import patch
from gpu.gpu import check_gpu_availability, _log_cuda_warning


class CudaWarningTest(unittest.TestCase):
    @patch('gpu.gpu.torch.cuda.is_available')
    @patch('gpu.gpu.settings')
    @patch('gpu.gpu.logger')
    def test_prints_warning_when_cuda_unavailable(self, mock_logger, mock_settings, mock_cuda):
        mock_cuda.return_value = False
        mock_settings.VERBOSE_OUTPUT = True
        
        check_gpu_availability()
        
        warning_printed = self.check_warning_was_logged(mock_logger)
        self.assertTrue(warning_printed)

    @patch('gpu.gpu.logger')
    def test_print_cuda_warning_outputs_message(self, mock_logger):
        _log_cuda_warning()

        mock_logger.warning.assert_called_once()
        call_args = mock_logger.warning.call_args[0][0]
        self.assertIn("CUDA", call_args)
        self.assertIn("CPU", call_args)

    def check_warning_was_logged(self, mock_logger) -> bool:
        return mock_logger.warning.called


if __name__ == "__main__":
    unittest.main()

