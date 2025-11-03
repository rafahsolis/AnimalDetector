from pathlib import Path
from typing import List
import argparse
import logging

logger = logging.getLogger(__name__)


class DatasetDirectoryCreator:
    def __init__(self, dataset_name: str, base_path: Path = Path('datasets')) -> None:
        self._dataset_name = dataset_name
        self._base_path = base_path
        self._dataset_root = base_path / dataset_name

    def create_structure(self) -> None:
        directories = self._get_required_directories()
        self._create_directories(directories)
        logger.info(f"✓ Created dataset structure for: {self._dataset_name}")

    def _get_required_directories(self) -> List[Path]:
        return [
            self._dataset_root / 'images',
            self._dataset_root / 'labels',
            self._dataset_root / 'train' / 'images',
            self._dataset_root / 'train' / 'labels',
            self._dataset_root / 'val' / 'images',
            self._dataset_root / 'val' / 'labels',
            self._dataset_root / 'test' / 'images',
            self._dataset_root / 'test' / 'labels'
        ]

    def _create_directories(self, directories: List[Path]) -> None:
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"Created: {directory}")


class ClassesFileInitializer:
    DEFAULT_CLASSES = [
        'bird',
        'wild_boar',
        'rabbit',
        'roe_deer',
        'fox',
        'human',
        'vehicle',
        'unknown_animal'
    ]

    def __init__(self, classes_file: Path) -> None:
        self._classes_file = classes_file

    def initialize_with_defaults(self) -> None:
        self._write_classes(self.DEFAULT_CLASSES)
        logger.info(f"✓ Created classes.txt with default animal classes")

    def initialize_with_custom(self, classes: List[str]) -> None:
        self._write_classes(classes)
        logger.info(f"✓ Created classes.txt with {len(classes)} custom classes")

    def _write_classes(self, classes: List[str]) -> None:
        self._classes_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._classes_file, 'w') as f:
            for class_name in classes:
                f.write(f"{class_name}\n")


class ReadmeGenerator:
    def __init__(self, dataset_root: Path, dataset_name: str) -> None:
        self._dataset_root = dataset_root
        self._dataset_name = dataset_name

    def create_readme(self) -> None:
        readme_path = self._dataset_root / 'README.md'
        content = self._generate_content()
        readme_path.write_text(content)
        logger.info(f"✓ Created README.md")

    def _generate_content(self) -> str:
        return f"""# {self._dataset_name}

## Dataset Information

- **Name:** {self._dataset_name}
- **Created:** $(date +%Y-%m-%d)
- **Purpose:** YOLOv11 object detection training

## Structure

```
{self._dataset_name}/
├── images/          # Original source images
├── labels/          # YOLO format annotations
│   └── classes.txt  # Class names (one per line)
├── train/           # Training set (70%)
│   ├── images/
│   └── labels/
├── val/             # Validation set (15%)
│   ├── images/
│   └── labels/
├── test/            # Test set (15%)
│   ├── images/
│   └── labels/
├── data.yaml        # YOLOv11 dataset config
└── README.md        # This file
```

## Workflow

### 1. Add Images

Place your images in the `images/` directory:

```bash
cp /path/to/your/images/* datasets/{self._dataset_name}/images/
```

### 2. Annotate with Label Studio

See [LABEL_STUDIO_GUIDE.md](../../docs/LABEL_STUDIO_GUIDE.md) for instructions.

### 3. Export and Convert

```bash
python -m yolo.label_studio_to_yolo \\
    --json export.json \\
    --images datasets/{self._dataset_name}/images \\
    --labels datasets/{self._dataset_name}/labels \\
    --classes datasets/{self._dataset_name}/labels/classes.txt
```

### 4. Validate Annotations

```bash
python -m yolo.validate_annotations \\
    --images datasets/{self._dataset_name}/images \\
    --labels datasets/{self._dataset_name}/labels \\
    --classes datasets/{self._dataset_name}/labels/classes.txt
```

### 5. Split Dataset

```bash
python -m yolo.split_dataset --dataset {self._dataset_name}
```

### 6. Generate data.yaml

```bash
python -m yolo.generate_data_yaml --dataset {self._dataset_name}
```

### 7. Train Model

```bash
python -m yolo.train_model
```

## Statistics

- **Total images:** TBD
- **Annotated images:** TBD
- **Total annotations:** TBD
- **Classes:** See `labels/classes.txt`

## Notes

Add any dataset-specific notes here:
- Camera locations
- Date ranges
- Known issues
- Special considerations

## Version History

- v1.0 (TBD): Initial dataset creation

"""


class DatasetInitializer:
    def __init__(self, dataset_name: str, custom_classes: List[str] = None) -> None:
        self._dataset_name = dataset_name
        self._custom_classes = custom_classes
        self._dataset_root = Path('datasets') / dataset_name

    def initialize(self) -> None:
        self._check_if_exists()
        self._create_directory_structure()
        self._initialize_classes_file()
        self._create_readme()
        self._print_summary()

    def _check_if_exists(self) -> None:
        if self._dataset_root.exists():
            logger.warning(f"Dataset already exists: {self._dataset_root}")
            response = input("Continue anyway? (y/n): ")
            if response.lower() != 'y':
                raise SystemExit("Aborted by user")

    def _create_directory_structure(self) -> None:
        creator = DatasetDirectoryCreator(self._dataset_name)
        creator.create_structure()

    def _initialize_classes_file(self) -> None:
        classes_file = self._dataset_root / 'labels' / 'classes.txt'
        initializer = ClassesFileInitializer(classes_file)
        
        if self._custom_classes:
            initializer.initialize_with_custom(self._custom_classes)
        else:
            initializer.initialize_with_defaults()

    def _create_readme(self) -> None:
        generator = ReadmeGenerator(self._dataset_root, self._dataset_name)
        generator.create_readme()

    def _print_summary(self) -> None:
        print(f"\n{'=' * 60}")
        print(f"✓ Dataset initialized: {self._dataset_name}")
        print(f"{'=' * 60}")
        print(f"\nLocation: {self._dataset_root}")
        print(f"\nNext steps:")
        print(f"1. Copy images to: {self._dataset_root / 'images'}/")
        print(f"2. Edit classes if needed: {self._dataset_root / 'labels' / 'classes.txt'}")
        print(f"3. Follow annotation guide: docs/LABEL_STUDIO_GUIDE.md")
        print(f"\nFor more info: cat {self._dataset_root / 'README.md'}")
        print()


def parse_classes_argument(classes_arg: str) -> List[str]:
    return [c.strip() for c in classes_arg.split(',') if c.strip()]


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Initialize a new dataset for YOLOv11 training'
    )
    parser.add_argument(
        'dataset_name',
        type=str,
        help='Name of the dataset (e.g., fototrampeo_bosque)'
    )
    parser.add_argument(
        '--classes',
        type=str,
        help='Comma-separated list of class names (e.g., "dog,cat,bird")'
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
    
    custom_classes = None
    if args.classes:
        custom_classes = parse_classes_argument(args.classes)
    
    try:
        initializer = DatasetInitializer(args.dataset_name, custom_classes)
        initializer.initialize()
    except Exception as e:
        logger.error(f"Failed to initialize dataset: {e}")
        raise


if __name__ == "__main__":
    main()

