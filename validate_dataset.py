from pathlib import Path
from typing import List, Dict
import yaml
class DatasetValidator:
    def __init__(self, dataset_root: Path) -> None:
        self._dataset_root = dataset_root
        self._errors: List[str] = []
        self._warnings: List[str] = []
    def validate(self) -> bool:
        self._validate_structure()
        self._validate_config_file()
        self._validate_image_label_pairs()
        self._validate_label_format()
        self._print_report()
        return len(self._errors) == 0
    def _validate_structure(self) -> None:
        required_dirs = [
            'train/images',
            'train/labels',
            'val/images',
            'val/labels',
        ]
        for dir_path in required_dirs:
            full_path = self._dataset_root / dir_path
            if not full_path.exists():
                self._errors.append(f"Missing required directory: {dir_path}")
    def _validate_config_file(self) -> None:
        config_path = self._dataset_root / 'data.yaml'
        if not config_path.exists():
            self._errors.append("Missing data.yaml configuration file")
            return
        self._validate_yaml_content(config_path)
    def _validate_yaml_content(self, config_path: Path) -> None:
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            self._check_required_yaml_keys(config)
        except Exception as e:
            self._errors.append(f"Error reading data.yaml: {str(e)}")
    def _check_required_yaml_keys(self, config: Dict) -> None:
        required_keys = ['path', 'train', 'val', 'nc', 'names']
        for key in required_keys:
            if key not in config:
                self._errors.append(f"Missing required key in data.yaml: {key}")
    def _validate_image_label_pairs(self) -> None:
        splits = ['train', 'val', 'test']
        for split in splits:
            self._check_split_pairs(split)
    def _check_split_pairs(self, split: str) -> None:
        images_dir = self._dataset_root / split / 'images'
        labels_dir = self._dataset_root / split / 'labels'
        if not images_dir.exists():
            return
        image_files = self._get_image_files(images_dir)
        self._check_matching_labels(image_files, labels_dir, split)
    def _get_image_files(self, images_dir: Path) -> List[Path]:
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(images_dir.glob(f'*{ext}'))
        return image_files
    def _check_matching_labels(
        self,
        image_files: List[Path],
        labels_dir: Path,
        split: str
    ) -> None:
        if len(image_files) == 0:
            self._warnings.append(f"No images found in {split}/images/")
            return
        missing_labels = self._find_missing_labels(image_files, labels_dir)
        if missing_labels:
            self._errors.append(
                f"{split}: {len(missing_labels)} images missing label files"
            )
    def _find_missing_labels(
        self,
        image_files: List[Path],
        labels_dir: Path
    ) -> List[Path]:
        missing = []
        for image_file in image_files:
            label_file = labels_dir / f"{image_file.stem}.txt"
            if not label_file.exists():
                missing.append(image_file)
        return missing
    def _validate_label_format(self) -> None:
        splits = ['train', 'val']
        for split in splits:
            self._check_split_labels(split)
    def _check_split_labels(self, split: str) -> None:
        labels_dir = self._dataset_root / split / 'labels'
        if not labels_dir.exists():
            return
        label_files = list(labels_dir.glob('*.txt'))
        if len(label_files) == 0:
            return
        sample_file = label_files[0]
        self._validate_label_file(sample_file, split)
    def _validate_label_file(self, label_file: Path, split: str) -> None:
        try:
            content = label_file.read_text().strip()
            if not content:
                self._warnings.append(
                    f"{split}: Empty label file found: {label_file.name}"
                )
                return
            lines = content.split('\n')
            for line in lines:
                self._validate_label_line(line, label_file, split)
        except Exception as e:
            self._errors.append(f"Error reading {label_file.name}: {str(e)}")
    def _validate_label_line(
        self,
        line: str,
        label_file: Path,
        split: str
    ) -> None:
        parts = line.split()
        if len(parts) != 5:
            self._errors.append(
                f"{split}/{label_file.name}: Invalid format (expected 5 values)"
            )
            return
        self._validate_label_values(parts, label_file, split)
    def _validate_label_values(
        self,
        parts: List[str],
        label_file: Path,
        split: str
    ) -> None:
        try:
            class_id = int(parts[0])
            coords = [float(x) for x in parts[1:5]]
            for coord in coords:
                if not (0.0 <= coord <= 1.0):
                    self._errors.append(
                        f"{split}/{label_file.name}: Coordinate out of range [0, 1]"
                    )
                    break
        except ValueError:
            self._errors.append(
                f"{split}/{label_file.name}: Non-numeric values found"
            )
    def _print_report(self) -> None:
        print("\n" + "=" * 70)
        print("DATASET VALIDATION REPORT")
        print("=" * 70)
        if len(self._errors) == 0 and len(self._warnings) == 0:
            print("✓ All checks passed! Dataset is ready for training.")
        else:
            self._print_errors()
            self._print_warnings()
            self._print_summary()
    def _print_errors(self) -> None:
        if self._errors:
            print(f"\n❌ ERRORS ({len(self._errors)}):")
            for error in self._errors:
                print(f"   - {error}")
    def _print_warnings(self) -> None:
        if self._warnings:
            print(f"\n⚠ WARNINGS ({len(self._warnings)}):")
            for warning in self._warnings:
                print(f"   - {warning}")
    def _print_summary(self) -> None:
        print("\n" + "=" * 70)
        if self._errors:
            print("❌ Dataset has errors. Please fix them before training.")
        else:
            print("✓ No errors found. Warnings are optional to fix.")
        print("=" * 70 + "\n")
def main() -> None:
    dataset_root = Path("datasets/animal_dataset")
    if not dataset_root.exists():
        print(f"❌ Dataset not found at: {dataset_root}")
        print("Run: python create_dataset_structure.py")
        return
    validator = DatasetValidator(dataset_root)
    is_valid = validator.validate()
    if not is_valid:
        exit(1)
if __name__ == "__main__":
    main()
