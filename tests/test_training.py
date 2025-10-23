import unittest
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from yolo.training import ModelTrainer


class ModelTrainerTest(unittest.TestCase):
    def setUp(self):
        self.model_path = Path("yolo/models/yolov8n.pt")
        self.device = "0"
        self.trainer = ModelTrainer(self.model_path, self.device)

    @patch('yolo.training.YOLO')
    def test_load_model_initializes_yolo_model(self, mock_yolo):
        self.trainer.load_model()
        
        mock_yolo.assert_called_once_with(str(self.model_path))

    @patch('yolo.training.YOLO')
    def test_train_executes_training_with_correct_args(self, mock_yolo):
        mock_model = self._create_mock_model()
        mock_yolo.return_value = mock_model
        
        data_config = Path("data.yaml")
        epochs = 10
        image_size = 640
        batch_size = 16
        
        self.trainer.train(data_config, epochs, image_size, batch_size)
        
        expected_args = self._get_expected_training_args(data_config, epochs, image_size, batch_size)
        mock_model.train.assert_called_once_with(**expected_args)

    def _create_mock_model(self):
        mock_model = MagicMock()
        mock_model.train.return_value = {}
        mock_model.val.return_value = {}
        return mock_model

    def _get_expected_training_args(self, data_config, epochs, image_size, batch_size):
        return {
            'data': str(data_config),
            'epochs': epochs,
            'imgsz': image_size,
            'batch': batch_size,
            'device': self.device
        }


if __name__ == "__main__":
    unittest.main()

