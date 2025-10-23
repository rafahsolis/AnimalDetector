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


def print_gpu_status(gpu_available: bool) -> None:
    print("=" * 50)
    print("GPU Configuration Check")
    print("=" * 50)
    print("=" * 50)


def get_device_name(device: str) -> str:
    if device == '0':
        return 'GPU (cuda:0)'
    return 'CPU'


def main() -> None:
    gpu_available = check_gpu_availability()
    print_gpu_status(gpu_available)

    device = settings.DEVICE if gpu_available else 'cpu'
    print(f"\nUsing device: {get_device_name(device)}\n")

    loader = ImageLoader(settings.IMAGE_FOLDER)
    detector = AnimalDetector(settings.MODEL_PATH, device=device)
    logger = ResultLogger(settings.LOG_FILE)

    pipeline = AnimalDetectionPipeline(loader, detector, logger)
    pipeline.run()

    print("\nDetection completed successfully!")


if __name__ == "__main__":
    main()

