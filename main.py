import os
os.environ.setdefault('SIMPLE_SETTINGS', 'settings,settings_local')

from yolo.yolo import (
    check_gpu_availability,
    ImageLoader,
    AnimalDetector,
    ResultLogger,
    AnimalDetectionPipeline
)
from simple_settings import settings
from yolo.logger_config import configure_logging, get_logger

configure_logging()
logger = get_logger('main')


def log_gpu_status() -> None:
    logger.info("=" * 50)
    logger.info("GPU Configuration Check")
    logger.info("=" * 50)


def get_device_name(device: str) -> str:
    if device == '0':
        return 'GPU (cuda:0)'
    return 'CPU'


def main() -> None:
    log_gpu_status()
    gpu_available = check_gpu_availability()
    logger.info("=" * 50)

    device = settings.DEVICE if gpu_available else 'cpu'
    device_name = get_device_name(device)
    logger.info(f"Using device: {device_name}")

    loader = ImageLoader(settings.IMAGE_FOLDER)
    detector = AnimalDetector(settings.MODEL_PATH, device=device)
    result_logger = ResultLogger(settings.LOG_FILE)

    pipeline = AnimalDetectionPipeline(loader, detector, result_logger)
    pipeline.run()

    logger.info("Detection completed successfully!")


if __name__ == "__main__":
    main()

