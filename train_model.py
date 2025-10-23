from pathlib import Path
from typing import Optional
from yolo.training import ModelTrainer
import logging

logger = logging.getLogger(__name__)


class TrainingConfiguration:
    def __init__(
        self,
        base_model_path: Path,
        data_config_path: Path,
        output_name: str,
        device: str
    ) -> None:
        self._base_model_path = base_model_path
        self._data_config_path = data_config_path
        self._output_name = output_name
        self._device = device

    @property
    def base_model_path(self) -> Path:
        return self._base_model_path

    @property
    def data_config_path(self) -> Path:
        return self._data_config_path

    @property
    def output_name(self) -> str:
        return self._output_name

    @property
    def device(self) -> str:
        return self._device


class TrainingParameters:
    def __init__(
        self,
        epochs: int = 100,
        image_size: int = 640,
        batch_size: int = 16
    ) -> None:
        self._epochs = epochs
        self._image_size = image_size
        self._batch_size = batch_size

    @property
    def epochs(self) -> int:
        return self._epochs

    @property
    def image_size(self) -> int:
        return self._image_size

    @property
    def batch_size(self) -> int:
        return self._batch_size


class ModelTrainingOrchestrator:
    def __init__(self, configuration: TrainingConfiguration) -> None:
        self._configuration = configuration
        self._trainer: Optional[ModelTrainer] = None

    def execute_training(self, parameters: TrainingParameters) -> None:
        self._initialize_trainer()
        self._log_training_start(parameters)
        self._run_training(parameters)
        self._log_training_complete()

    def _initialize_trainer(self) -> None:
        self._trainer = ModelTrainer(
            self._configuration.base_model_path,
            self._configuration.device
        )

    def _log_training_start(self, parameters: TrainingParameters) -> None:
        logger.info("=" * 80)
        logger.info("STARTING MODEL TRAINING")
        logger.info(f"Base model: {self._configuration.base_model_path}")
        logger.info(f"Dataset config: {self._configuration.data_config_path}")
        logger.info(f"Device: {self._configuration.device}")
        logger.info(f"Epochs: {parameters.epochs}")
        logger.info(f"Image size: {parameters.image_size}")
        logger.info(f"Batch size: {parameters.batch_size}")
        logger.info("=" * 80)

    def _run_training(self, parameters: TrainingParameters) -> None:
        self._trainer.train(
            data_config=self._configuration.data_config_path,
            epochs=parameters.epochs,
            image_size=parameters.image_size,
            batch_size=parameters.batch_size
        )

    def _log_training_complete(self) -> None:
        logger.info("=" * 80)
        logger.info("TRAINING COMPLETED SUCCESSFULLY")
        logger.info("Results saved to: runs/detect/train/")
        logger.info("Best model: runs/detect/train/weights/best.pt")
        logger.info("Last model: runs/detect/train/weights/last.pt")
        logger.info("=" * 80)


def main() -> None:
    configuration = create_training_configuration()
    parameters = create_training_parameters()
    orchestrator = ModelTrainingOrchestrator(configuration)
    orchestrator.execute_training(parameters)


def create_training_configuration() -> TrainingConfiguration:
    base_model_path = Path("yolo/models/yolo11n.pt")
    data_config_path = Path("datasets/animal_dataset/data.yaml")
    output_name = "custom_animal_detector"
    device = "0"
    
    return TrainingConfiguration(
        base_model_path,
        data_config_path,
        output_name,
        device
    )


def create_training_parameters() -> TrainingParameters:
    epochs = 100
    image_size = 640
    batch_size = 16
    
    return TrainingParameters(epochs, image_size, batch_size)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    main()

