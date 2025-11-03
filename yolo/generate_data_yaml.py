from pathlib import Path
from typing import List
import yaml
import argparse
import logging

logger = logging.getLogger(__name__)


class ClassesLoader:
    @staticmethod
    def load_from_file(classes_file: Path) -> List[str]:
        if not classes_file.exists():
            raise FileNotFoundError(f"Classes file not found: {classes_file}")

        with open(classes_file, 'r') as f:
            classes = [line.strip() for line in f if line.strip()]

        if not classes:
            raise ValueError("Classes file is empty")

        return classes


class DataYAMLGenerator:
    def __init__(self, dataset_root: Path, classes_file: Path) -> None:
        self._dataset_root = dataset_root.resolve()
        self._classes = ClassesLoader.load_from_file(classes_file)

    def generate(self) -> str:
        data_config = self._build_config_dict()
        return yaml.dump(data_config, default_flow_style=False, sort_keys=False)

    def _build_config_dict(self) -> dict:
        return {
            'path': str(self._dataset_root),
            'train': 'train/images',
            'val': 'val/images',
            'test': 'test/images',
            'nc': len(self._classes),
            'names': self._classes
        }

    def save_to_file(self, output_path: Path) -> None:
        yaml_content = self.generate()
        output_path.write_text(yaml_content)
        logger.info(f"✓ data.yaml created at: {output_path}")


def validate_directory_structure(dataset_root: Path) -> None:
    required_dirs = [
        dataset_root / 'train' / 'images',
        dataset_root / 'train' / 'labels',
        dataset_root / 'val' / 'images',
        dataset_root / 'val' / 'labels'
    ]

    missing_dirs = [d for d in required_dirs if not d.exists()]

    if missing_dirs:
        logger.warning("Some directories are missing:")
        for d in missing_dirs:
            logger.warning(f"  - {d}")
        logger.warning("Run 'python -m yolo.split_dataset' first")


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Generate data.yaml for YOLOv11 training'
    )
    parser.add_argument(
        '--dataset',
        type=str,
        required=True,
        help='Dataset name (e.g., fototrampeo_bosque)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Output path for data.yaml (default: dataset_root/data.yaml)'
    )
    return parser


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )


def main() -> None:
    configure_logging()
    parser = create_argument_parser()
    args = parser.parse_args()

    dataset_root = Path('datasets') / args.dataset
    classes_file = dataset_root / 'labels' / 'classes.txt'

    if not dataset_root.exists():
        logger.error(f"Dataset not found: {dataset_root}")
        return

    validate_directory_structure(dataset_root)

    output_path = args.output or dataset_root / 'data.yaml'

    try:
        generator = DataYAMLGenerator(dataset_root, classes_file)
        generator.save_to_file(output_path)

        print(f"\n✓ Generated data.yaml for YOLOv11 training:")
        print(f"  Location: {output_path}")
        print(f"\nContent preview:")
        print(generator.generate())

    except Exception as e:
        logger.error(f"Failed to generate data.yaml: {e}")
        raise


if __name__ == "__main__":
    main()

