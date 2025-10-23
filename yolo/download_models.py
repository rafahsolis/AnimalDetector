#!/usr/bin/env python3
"""
Script to download YOLO models to the yolo/models directory.

Usage:
    python -m yolo.download_models                    # Download all detection models (v8 and v11, all sizes)
    python -m yolo.download_models yolov8n.pt         # Download specific model
    python -m yolo.download_models --all              # Download ALL available models (detection, seg, pose, cls, obb)
    python -m yolo.download_models --detection        # Download all detection models
    python -m yolo.download_models --segmentation     # Download all segmentation models
    python -m yolo.download_models --pose             # Download all pose models
    python -m yolo.download_models --classification   # Download all classification models
    python -m yolo.download_models --obb              # Download all OBB models
"""
import sys
import logging
from yolo import ModelDownloader
from settings import MODELS_DIR

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


def download_specific_model(model_name: str) -> None:
    downloader = ModelDownloader(MODELS_DIR)
    downloader.download_model(model_name)


def download_by_category(category: str) -> None:
    downloader = ModelDownloader(MODELS_DIR)

    category_map = {
        '--all': downloader.download_all_available_models,
        '--detection': downloader.download_all_detection_models,
        '--segmentation': downloader.download_all_segmentation_models,
        '--pose': downloader.download_all_pose_models,
        '--classification': downloader.download_all_classification_models,
        '--obb': downloader.download_all_obb_models
    }

    download_func = category_map.get(category)
    if download_func:
        download_func()
    else:
        print_usage_and_exit()


def print_usage_and_exit() -> None:
    print(__doc__)
    sys.exit(1)


def download_standard_models() -> None:
    downloader = ModelDownloader(MODELS_DIR)
    downloader.download_all_detection_models()


def main() -> None:
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.startswith('--'):
            download_by_category(arg)
        else:
            download_specific_model(arg)
    else:
        download_standard_models()


if __name__ == "__main__":
    main()

