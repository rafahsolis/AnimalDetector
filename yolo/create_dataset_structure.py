from pathlib import Path
import shutil
import argparse


class DatasetStructureCreator:
    README_TEMPLATE_PATH = Path(__file__).parent / 'templates' / 'datasets' / 'README_TEMPLATE.md'
    DATASETS_ROOT = Path('datasets')

    def __init__(self, dataset_name: str) -> None:
        self._dataset_name = dataset_name
        self._dataset_root = self.DATASETS_ROOT / dataset_name

    def create_structure(self) -> None:
        self._create_root_directory()
        self._create_source_directories()
        self._create_readme()
        self._log_completion()

    def _create_root_directory(self) -> None:
        self._dataset_root.mkdir(parents=True, exist_ok=True)

    def _create_source_directories(self) -> None:
        images_path = self._dataset_root / 'images'
        labels_path = self._dataset_root / 'labels'
        images_path.mkdir(parents=True, exist_ok=True)
        labels_path.mkdir(parents=True, exist_ok=True)

    def _create_readme(self) -> None:
        readme_path = self._dataset_root / 'README.md'
        self._copy_readme_template(readme_path)

    def _copy_readme_template(self, destination: Path) -> None:
        if self.README_TEMPLATE_PATH.exists():
            shutil.copy2(self.README_TEMPLATE_PATH, destination)

    def _log_completion(self) -> None:
        self._log_success_message()
        self._log_created_directories()
        self._log_workflow_steps()
        self._log_help_message()

    def _log_success_message(self) -> None:
        print(f"✓ Dataset structure created at: {self._dataset_root}")

    def _log_created_directories(self) -> None:
        print("\nCreated directories:")
        print(f"  - {self._dataset_root / 'images'}")
        print(f"  - {self._dataset_root / 'labels'}")

    def _log_workflow_steps(self) -> None:
        print("\n📋 Simplified Workflow:")
        print(f"  1. Add images to: {self._dataset_root / 'images'}")
        print(f"  2. Annotate: labelImg {self._dataset_root / 'images'} {self._dataset_root / 'labels'}")
        print(f"  3. Split dataset: python -m yolo.split_dataset --dataset {self._dataset_name}")
        print("  4. Configure: cp data.yaml.example data.yaml")
        print("  5. Download models: python -m yolo.download_models")
        print("  6. Train: python -m yolo.train_model")

    def _log_help_message(self) -> None:
        print("\n📖 See README.md for detailed instructions")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Create dataset structure for YOLO training'
    )
    parser.add_argument(
        '--dataset',
        type=str,
        default='image_dataset',
        help='Name of the dataset (default: image_dataset)'
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    creator = DatasetStructureCreator(args.dataset)
    creator.create_structure()


if __name__ == "__main__":
    main()


