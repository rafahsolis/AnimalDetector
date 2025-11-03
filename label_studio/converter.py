import json
import hashlib
from pathlib import Path
from typing import List, Dict, Set, Tuple
import argparse
import logging

logger = logging.getLogger(__name__)


class ClassMapper:
    def __init__(self, classes_file: Path) -> None:
        self._classes_file = classes_file
        self._classes = self._load_classes()

    def _load_classes(self) -> List[str]:
        if not self._classes_file.exists():
            raise FileNotFoundError(f"Classes file not found: {self._classes_file}")
        
        with open(self._classes_file, 'r') as file:
            classes = [line.strip() for line in file if line.strip()]
        
        return classes

    def get_class_id(self, class_name: str) -> int:
        if class_name not in self._classes:
            raise ValueError(f"Unknown class: {class_name}")
        return self._classes.index(class_name)

    def get_all_classes(self) -> List[str]:
        return self._classes.copy()


class BoundingBoxConverter:
    @staticmethod
    def label_studio_to_yolo(
            x: float,
            y: float,
            width: float,
            height: float,
            img_width: int,
            img_height: int
    ) -> Tuple[float, float, float, float]:
        x_center = (x + width / 2) / 100.0
        y_center = (y + height / 2) / 100.0
        norm_width = width / 100.0
        norm_height = height / 100.0
        
        return x_center, y_center, norm_width, norm_height

    @staticmethod
    def validate_box(cx: float, cy: float, w: float, h: float) -> bool:
        return all(0 <= val <= 1 for val in [cx, cy, w, h])


class AnnotationExtractor:
    def __init__(self, class_mapper: ClassMapper) -> None:
        self._class_mapper = class_mapper

    def extract_from_task(self, task: Dict) -> List[str]:
        if not task.get('annotations'):
            return []
        
        latest_annotation = task['annotations'][-1]
        
        if not latest_annotation.get('result'):
            return []
        
        yolo_lines = []
        for result in latest_annotation['result']:
            if result.get('type') != 'rectanglelabels':
                continue
            
            yolo_line = self._convert_rectangle_to_yolo(result)
            if yolo_line:
                yolo_lines.append(yolo_line)
        
        return yolo_lines

    def _convert_rectangle_to_yolo(self, result: Dict) -> str:
        value = result.get('value', {})
        labels = value.get('rectanglelabels', [])
        
        if not labels:
            return ""
        
        class_name = labels[0]
        class_id = self._class_mapper.get_class_id(class_name)
        
        original_width = result.get('original_width', 100)
        original_height = result.get('original_height', 100)
        
        x = value.get('x', 0)
        y = value.get('y', 0)
        width = value.get('width', 0)
        height = value.get('height', 0)
        
        cx, cy, w, h = BoundingBoxConverter.label_studio_to_yolo(
            x, y, width, height, original_width, original_height
        )
        
        if not BoundingBoxConverter.validate_box(cx, cy, w, h):
            logger.warning(f"Invalid bounding box: {cx} {cy} {w} {h}")
            return ""
        
        return f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"


class ImageHasher:
    @staticmethod
    def compute_hash(file_path: Path) -> str:
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()


class DuplicateDetector:
    def __init__(self) -> None:
        self._seen_hashes: Set[str] = set()

    def is_duplicate(self, file_path: Path) -> bool:
        file_hash = ImageHasher.compute_hash(file_path)
        
        if file_hash in self._seen_hashes:
            return True
        
        self._seen_hashes.add(file_hash)
        return False


class FilePathResolver:
    def __init__(self, images_dir: Path) -> None:
        self._images_dir = images_dir

    def find_image_file(self, filename: str) -> Path:
        image_path = self._images_dir / filename
        
        if image_path.exists():
            return image_path
        
        for ext in ['.JPG', '.jpg', '.PNG', '.png', '.JPEG', '.jpeg']:
            candidate = image_path.with_suffix(ext)
            if candidate.exists():
                return candidate
        
        raise FileNotFoundError(f"Image not found: {filename}")


class LabelStudioToYOLOConverter:
    def __init__(
            self,
            json_export: Path,
            images_dir: Path,
            labels_dir: Path,
            classes_file: Path,
            skip_duplicates: bool = True
    ) -> None:
        self._json_export = json_export
        self._images_dir = images_dir
        self._labels_dir = labels_dir
        self._class_mapper = ClassMapper(classes_file)
        self._skip_duplicates = skip_duplicates
        self._duplicate_detector = DuplicateDetector() if skip_duplicates else None
        self._annotation_extractor = AnnotationExtractor(self._class_mapper)
        self._path_resolver = FilePathResolver(images_dir)

    def convert(self) -> None:
        self._prepare_labels_directory()
        tasks = self._load_tasks()
        self._process_tasks(tasks)

    def _prepare_labels_directory(self) -> None:
        self._labels_dir.mkdir(parents=True, exist_ok=True)

    def _load_tasks(self) -> List[Dict]:
        with open(self._json_export, 'r') as f:
            return json.load(f)

    def _process_tasks(self, tasks: List[Dict]) -> None:
        total = len(tasks)
        processed = 0
        skipped_duplicates = 0
        skipped_no_annotations = 0
        errors = 0
        
        for task in tasks:
            try:
                if self._process_single_task(task):
                    processed += 1
                else:
                    if self._is_duplicate(task):
                        skipped_duplicates += 1
                    else:
                        skipped_no_annotations += 1
            except Exception as e:
                logger.error(f"Error processing task: {e}")
                errors += 1
        
        self._log_summary(total, processed, skipped_duplicates, skipped_no_annotations, errors)

    def _process_single_task(self, task: Dict) -> bool:
        image_filename = self._extract_image_filename(task)
        image_path = self._path_resolver.find_image_file(image_filename)
        
        if self._should_skip_duplicate(image_path):
            return False
        
        yolo_annotations = self._annotation_extractor.extract_from_task(task)
        
        if not yolo_annotations and not self._task_has_annotations(task):
            return False
        
        self._write_label_file(image_filename, yolo_annotations)
        return True

    def _extract_image_filename(self, task: Dict) -> str:
        image_url = task.get('data', {}).get('image', '')
        return Path(image_url).name

    def _should_skip_duplicate(self, image_path: Path) -> bool:
        if not self._skip_duplicates:
            return False
        return self._duplicate_detector.is_duplicate(image_path)

    def _is_duplicate(self, task: Dict) -> bool:
        if not self._skip_duplicates:
            return False
        image_filename = self._extract_image_filename(task)
        image_path = self._path_resolver.find_image_file(image_filename)
        return self._duplicate_detector.is_duplicate(image_path)

    def _task_has_annotations(self, task: Dict) -> bool:
        return bool(task.get('annotations'))

    def _write_label_file(self, image_filename: str, yolo_lines: List[str]) -> None:
        label_filename = Path(image_filename).stem + '.txt'
        label_path = self._labels_dir / label_filename
        
        with open(label_path, 'w') as f:
            f.write('\n'.join(yolo_lines))
            if yolo_lines:
                f.write('\n')

    def _log_summary(
            self,
            total: int,
            processed: int,
            skipped_duplicates: int,
            skipped_no_annotations: int,
            errors: int
    ) -> None:
        logger.info(f"Conversion summary:")
        logger.info(f"  Total tasks: {total}")
        logger.info(f"  Processed: {processed}")
        logger.info(f"  Skipped (duplicates): {skipped_duplicates}")
        logger.info(f"  Skipped (no annotations): {skipped_no_annotations}")
        logger.info(f"  Errors: {errors}")


def create_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Convert Label Studio JSON export to YOLO format'
    )
    parser.add_argument(
        '--json',
        type=Path,
        required=True,
        help='Path to Label Studio JSON export file'
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
        help='Path to output labels directory'
    )
    parser.add_argument(
        '--classes',
        type=Path,
        required=True,
        help='Path to classes.txt file'
    )
    parser.add_argument(
        '--skip-duplicates',
        action='store_true',
        default=True,
        help='Skip duplicate images (default: True)'
    )
    return parser


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def main() -> None:
    configure_logging()
    parser = create_argument_parser()
    args = parser.parse_args()
    
    converter = LabelStudioToYOLOConverter(
        json_export=args.json,
        images_dir=args.images,
        labels_dir=args.labels,
        classes_file=args.classes,
        skip_duplicates=args.skip_duplicates
    )
    
    try:
        converter.convert()
        logger.info("✓ Conversion completed successfully!")
    except Exception as e:
        logger.error(f"✗ Conversion failed: {e}")
        raise


if __name__ == "__main__":
    main()

