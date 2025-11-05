from pathlib import Path
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import argparse
import logging

logger = logging.getLogger(__name__)


class YOLOLabelParser:
    @staticmethod
    def parse_line(line: str) -> Tuple[int, float, float, float, float]:
        parts = line.strip().split()
        if len(parts) != 5:
            raise ValueError(f"Invalid YOLO format: {line}")
        
        class_id = int(parts[0])
        cx = float(parts[1])
        cy = float(parts[2])
        w = float(parts[3])
        h = float(parts[4])
        
        return class_id, cx, cy, w, h

    @staticmethod
    def validate_coordinates(cx: float, cy: float, w: float, h: float) -> bool:
        return all(0 <= val <= 1 for val in [cx, cy, w, h])


class BoxSizeCalculator:
    @staticmethod
    def calculate_area(width: float, height: float) -> float:
        return width * height

    @staticmethod
    def categorize_by_area(area: float) -> str:
        if area < 0.01:
            return "tiny"
        if area < 0.05:
            return "small"
        if area < 0.20:
            return "medium"
        return "large"


class DatasetStatistics:
    def __init__(self, classes: List[str]) -> None:
        self._classes = classes
        self._class_counts: Dict[int, int] = defaultdict(int)
        self._images_per_class: Dict[int, Set[str]] = defaultdict(set)
        self._box_sizes: List[Tuple[float, int]] = []
        self._total_images = 0
        self._empty_images = 0
        self._total_annotations = 0
        self._invalid_boxes = 0
        self._duplicate_boxes: Dict[str, int] = defaultdict(int)

    def process_label_file(self, label_path: Path, image_name: str) -> None:
        self._total_images += 1
        
        if not label_path.exists():
            self._empty_images += 1
            return
        
        with open(label_path, 'r') as f:
            lines = f.readlines()
        
        if not lines or all(not line.strip() for line in lines):
            self._empty_images += 1
            return
        
        image_boxes = set()
        for line in lines:
            if not line.strip():
                continue
            
            try:
                self._process_annotation_line(line, image_name, image_boxes)
            except ValueError as e:
                logger.warning(f"Skipping invalid line in {label_path}: {e}")
                self._invalid_boxes += 1

    def _process_annotation_line(
            self,
            line: str,
            image_name: str,
            image_boxes: Set[str]
    ) -> None:
        class_id, cx, cy, w, h = YOLOLabelParser.parse_line(line)
        
        if not YOLOLabelParser.validate_coordinates(cx, cy, w, h):
            self._invalid_boxes += 1
            logger.warning(f"Invalid coordinates in {image_name}: {line.strip()}")
            return
        
        box_key = f"{class_id}_{cx:.4f}_{cy:.4f}_{w:.4f}_{h:.4f}"
        if box_key in image_boxes:
            self._duplicate_boxes[image_name] += 1
            return
        
        image_boxes.add(box_key)
        
        self._class_counts[class_id] += 1
        self._images_per_class[class_id].add(image_name)
        
        area = BoxSizeCalculator.calculate_area(w, h)
        self._box_sizes.append((area, class_id))
        
        self._total_annotations += 1

    def generate_report(self) -> str:
        lines = []
        lines.append("=" * 60)
        lines.append("YOLO Dataset Validation Report")
        lines.append("=" * 60)
        lines.append("")
        
        lines.extend(self._generate_overview_section())
        lines.append("")
        lines.extend(self._generate_class_distribution_section())
        lines.append("")
        lines.extend(self._generate_box_size_section())
        lines.append("")
        lines.extend(self._generate_warnings_section())
        
        return "\n".join(lines)

    def _generate_overview_section(self) -> List[str]:
        lines = []
        lines.append("Overview:")
        lines.append(f"  Total images: {self._total_images}")
        lines.append(f"  Images with annotations: {self._total_images - self._empty_images}")
        lines.append(f"  Empty images: {self._empty_images}")
        lines.append(f"  Total annotations: {self._total_annotations}")
        
        if self._total_images > 0:
            avg_annotations = self._total_annotations / self._total_images
            lines.append(f"  Average annotations per image: {avg_annotations:.2f}")
        
        return lines

    def _generate_class_distribution_section(self) -> List[str]:
        lines = []
        lines.append("Class Distribution:")
        
        for class_id in sorted(self._class_counts.keys()):
            class_name = self._get_class_name(class_id)
            count = self._class_counts[class_id]
            num_images = len(self._images_per_class[class_id])
            percentage = self._calculate_percentage(count)
            
            lines.append(
                f"  {class_name:20} | "
                f"Boxes: {count:5} ({percentage:5.1f}%) | "
                f"Images: {num_images:4}"
            )
        
        return lines

    def _generate_box_size_section(self) -> List[str]:
        lines = []
        lines.append("Bounding Box Size Distribution:")
        
        size_categories = defaultdict(int)
        for area, _ in self._box_sizes:
            category = BoxSizeCalculator.categorize_by_area(area)
            size_categories[category] += 1
        
        for size in ["tiny", "small", "medium", "large"]:
            count = size_categories.get(size, 0)
            percentage = self._calculate_percentage(count)
            lines.append(f"  {size.capitalize():10} (<{self._get_size_threshold(size):5.1%}): {count:5} ({percentage:5.1f}%)")
        
        return lines

    def _generate_warnings_section(self) -> List[str]:
        lines = []
        
        if self._invalid_boxes > 0:
            lines.append(f"⚠ WARNING: {self._invalid_boxes} invalid bounding boxes detected!")
        
        if sum(self._duplicate_boxes.values()) > 0:
            total_dupes = sum(self._duplicate_boxes.values())
            lines.append(f"⚠ WARNING: {total_dupes} duplicate boxes in {len(self._duplicate_boxes)} images")
        
        missing_classes = self._find_missing_classes()
        if missing_classes:
            lines.append(f"⚠ WARNING: No annotations for classes: {', '.join(missing_classes)}")
        
        if not lines:
            lines.append("✓ No warnings detected")
        
        return lines

    def _get_class_name(self, class_id: int) -> str:
        if 0 <= class_id < len(self._classes):
            return self._classes[class_id]
        return f"unknown_{class_id}"

    def _calculate_percentage(self, count: int) -> float:
        if self._total_annotations == 0:
            return 0.0
        return (count / self._total_annotations) * 100

    def _get_size_threshold(self, size: str) -> float:
        thresholds = {"tiny": 0.01, "small": 0.05, "medium": 0.20, "large": 1.0}
        return thresholds.get(size, 1.0)

    def _find_missing_classes(self) -> List[str]:
        missing = []
        for i, class_name in enumerate(self._classes):
            if i not in self._class_counts or self._class_counts[i] == 0:
                missing.append(class_name)
        return missing


class DatasetValidator:
    def __init__(self, images_dir: Path, labels_dir: Path, classes_file: Path) -> None:
        self._images_dir = images_dir
        self._labels_dir = labels_dir
        self._classes = self._load_classes(classes_file)
        self._statistics = DatasetStatistics(self._classes)

    def _load_classes(self, classes_file: Path) -> List[str]:
        with open(classes_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]

    def validate(self) -> str:
        image_files = self._find_image_files()
        
        for image_file in image_files:
            label_file = self._get_corresponding_label_file(image_file)
            self._statistics.process_label_file(label_file, image_file.name)
        
        return self._statistics.generate_report()

    def _find_image_files(self) -> List[Path]:
        extensions = ['*.jpg', '*.JPG', '*.jpeg', '*.JPEG', '*.png', '*.PNG']
        image_files = []
        
        for ext in extensions:
            image_files.extend(self._images_dir.glob(ext))
        
        return sorted(image_files)

    def _get_corresponding_label_file(self, image_file: Path) -> Path:
        label_name = image_file.stem + '.txt'
        return self._labels_dir / label_name


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Validate YOLO dataset and generate statistics report'
    )
    parser.add_argument(
        '--images',
        type=Path,
        required=True,
        help='Path to images directory'
    )
    parser.add_argument(
        '--labels',
        type=Path,
        required=True,
        help='Path to labels directory'
    )
    parser.add_argument(
        '--classes',
        type=Path,
        required=True,
        help='Path to classes.txt file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        help='Path to save report (optional, prints to console if not specified)'
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
    
    validator = DatasetValidator(
        images_dir=args.images,
        labels_dir=args.labels,
        classes_file=args.classes
    )
    
    try:
        report = validator.validate()
        
        if args.output:
            args.output.write_text(report)
            logger.info(f"✓ Report saved to: {args.output}")
        else:
            print(report)
        
    except Exception as e:
        logger.error(f"✗ Validation failed: {e}")
        raise


if __name__ == "__main__":
    main()

