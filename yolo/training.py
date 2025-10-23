from pathlib import Path
from typing import Dict, Any, Optional
from ultralytics import YOLO
import logging

logger = logging.getLogger(__name__)


class ModelTrainer:
    def __init__(self, model_path: Path, device: str) -> None:
        self._model_path = model_path
        self._device = device
        self._model = None

    def load_model(self) -> None:
        logger.info(f"Loading YOLO model from {self._model_path}")
        self._model = YOLO(str(self._model_path))

    def train(self, data_config: Path, epochs: int, image_size: int, batch_size: int) -> Dict[str, Any]:
        if self._model is None:
            self.load_model()
        
        training_args = self._build_training_args(data_config, epochs, image_size, batch_size)
        results = self._execute_training(training_args)
        return results

    def _build_training_args(self, data_config: Path, epochs: int, image_size: int, batch_size: int) -> Dict[str, Any]:
        return {
            'data': str(data_config),
            'epochs': epochs,
            'imgsz': image_size,
            'batch': batch_size,
            'device': self._device
        }

    def _execute_training(self, training_args: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Starting training with args: {training_args}")
        results = self._model.train(**training_args)
        logger.info("Training completed successfully")
        return results

    def save_model(self, output_path: Path) -> None:
        if self._model is None:
            raise ValueError("No model loaded to save")
        
        logger.info(f"Saving model to {output_path}")
        self._model.save(str(output_path))

    def evaluate(self, data_config: Optional[Path] = None) -> Dict[str, Any]:
        if self._model is None:
            self.load_model()
        
        evaluation_args = self._build_evaluation_args(data_config)
        results = self._execute_evaluation(evaluation_args)
        return results

    def _build_evaluation_args(self, data_config: Optional[Path]) -> Dict[str, Any]:
        args = {'device': self._device}
        if data_config is not None:
            args['data'] = str(data_config)
        return args

    def _execute_evaluation(self, evaluation_args: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"Starting evaluation with args: {evaluation_args}")
        results = self._model.val(**evaluation_args)
        logger.info("Evaluation completed successfully")
        return results

