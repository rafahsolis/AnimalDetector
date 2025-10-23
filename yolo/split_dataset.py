from pathlib import Path
from typing import List, Tuple
import random
import shutil
import logging

logger = logging.getLogger(__name__)


class SplitRatios:
    def __init__(
        self,
        train: float = 0.7,
        val: float = 0.15,
        test: float = 0.15
    ) -> None:
        self._train = train
        self._val = val
        self._test = test
        self._validate_ratios()

    def _validate_ratios(self) -> None:
        total = self._train + self._val + self._test
        if not abs(total - 1.0) < 0.001:
            raise ValueError(f"Split ratios must sum to 1.0, got {total}")

    @property
    def train(self) -> float:
        return self._train

    @property
    def val(self) -> float:
        return self._val

    @property
    def test(self) -> float:
        return self._test


class DatasetPaths:
    def __init__(self, dataset_root: Path) -> None:
        self._dataset_root = dataset_root

    @property
    def images_source(self) -> Path:
        return self._dataset_root / 'images'

    @property
    def labels_source(self) -> Path:
        return self._dataset_root / 'labels'

    @property
    def train_images(self) -> Path:
        return self._dataset_root / 'train' / 'images'

    @property
    def train_labels(self) -> Path:
        return self._dataset_root / 'train' / 'labels'

    @property
    def val_images(self) -> Path:
        return self._dataset_root / 'val' / 'images'

    @property
    def val_labels(self) -> Path:
        return self._dataset_root / 'val' / 'labels'

    @property
    def test_images(self) -> Path:
        return self._dataset_root / 'test' / 'images'

    @property
    def test_labels(self) -> Path:
        return self._dataset_root / 'test' / 'labels'


class ImageFileFinder:
    SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

    def __init__(self, source_path: Path) -> None:
        self._source_path = source_path

    def find_all_images(self) -> List[Path]:
        if not self._source_path.exists():
            return []
        
        images = []
        for file_path in self._source_path.iterdir():
            if self._is_image_file(file_path):
                images.append(file_path)
        
        return sorted(images)

    def _is_image_file(self, file_path: Path) -> bool:
        return file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS


class DatasetSplitter:
    def __init__(
        self,
        paths: DatasetPaths,
        ratios: SplitRatios,
        random_seed: int = 42
    ) -> None:
        self._paths = paths
        self._ratios = ratios
        self._random_seed = random_seed

    def split(self) -> None:
        self._validate_source_folders()
        self._clear_destination_folders()
        self._create_destination_folders()
        
        images = self._get_images_to_split()
        self._shuffle_images(images)
        
        splits = self._calculate_split_indices(len(images))
        self._move_files_to_splits(images, splits)
        self._log_summary(len(images), splits)

    def _validate_source_folders(self) -> None:
        if not self._paths.images_source.exists():
            raise FileNotFoundError(
                f"Images folder not found: {self._paths.images_source}"
            )

    def _clear_destination_folders(self) -> None:
        folders_to_clear = [
            self._paths.train_images,
            self._paths.train_labels,
            self._paths.val_images,
            self._paths.val_labels,
            self._paths.test_images,
            self._paths.test_labels,
        ]
        
        for folder in folders_to_clear:
            if folder.exists():
                shutil.rmtree(folder)

    def _create_destination_folders(self) -> None:
        folders_to_create = [
            self._paths.train_images,
            self._paths.train_labels,
            self._paths.val_images,
            self._paths.val_labels,
            self._paths.test_images,
            self._paths.test_labels,
        ]
        
        for folder in folders_to_create:
            folder.mkdir(parents=True, exist_ok=True)

    def _get_images_to_split(self) -> List[Path]:
        finder = ImageFileFinder(self._paths.images_source)
        images = finder.find_all_images()
        
        if not images:
            raise ValueError(
                f"No images found in {self._paths.images_source}"
            )
        
        return images

    def _shuffle_images(self, images: List[Path]) -> None:
        random.seed(self._random_seed)
        random.shuffle(images)

    def _calculate_split_indices(self, total_images: int) -> Tuple[int, int]:
        train_end = int(total_images * self._ratios.train)
        val_end = train_end + int(total_images * self._ratios.val)
        return train_end, val_end

    def _move_files_to_splits(
        self,
        images: List[Path],
        splits: Tuple[int, int]
    ) -> None:
        train_end, val_end = splits
        
        self._move_image_batch(
            images[:train_end],
            self._paths.train_images,
            self._paths.train_labels
        )
        self._move_image_batch(
            images[train_end:val_end],
            self._paths.val_images,
            self._paths.val_labels
        )
        self._move_image_batch(
            images[val_end:],
            self._paths.test_images,
            self._paths.test_labels
        )

    def _move_image_batch(
        self,
        images: List[Path],
        dest_images: Path,
        dest_labels: Path
    ) -> None:
        for image in images:
            self._move_image_file(image, dest_images)
            self._move_label_file(image, dest_labels)

    def _move_image_file(self, image: Path, destination: Path) -> None:
        dest_path = destination / image.name
        shutil.copy2(str(image), str(dest_path))

    def _move_label_file(self, image: Path, destination: Path) -> None:
        label_name = image.stem + '.txt'
        label_path = self._paths.labels_source / label_name
        
        if not label_path.exists():
            logger.warning(f"Label not found for {image.name}")
            return
        
        dest_path = destination / label_name
        shutil.copy2(str(label_path), str(dest_path))

    def _log_summary(self, total: int, splits: Tuple[int, int]) -> None:
        train_end, val_end = splits
        train_count = train_end
        val_count = val_end - train_end
        test_count = total - val_end
        
        logger.info(f"Dataset split completed:")
        logger.info(f"  Train: {train_count} images ({train_count/total*100:.1f}%)")
        logger.info(f"  Val:   {val_count} images ({val_count/total*100:.1f}%)")
        logger.info(f"  Test:  {test_count} images ({test_count/total*100:.1f}%)")
        logger.info(f"  Total: {total} images")


def create_default_ratios() -> SplitRatios:
    return SplitRatios(train=0.7, val=0.15, test=0.15)


def create_dataset_paths() -> DatasetPaths:
    dataset_root = Path("datasets/animal_dataset")
    return DatasetPaths(dataset_root)


def main() -> None:
    paths = create_dataset_paths()
    ratios = create_default_ratios()
    splitter = DatasetSplitter(paths, ratios, random_seed=42)
    
    try:
        splitter.split()
        print("\n✓ Dataset split completed successfully!")
        print(f"\nSource folders (preserved):")
        print(f"  - {paths.images_source}")
        print(f"  - {paths.labels_source}")
        print(f"\nDestination folders:")
        print(f"  - {paths.train_images}")
        print(f"  - {paths.val_images}")
        print(f"  - {paths.test_images}")
        print("\nNext steps:")
        print("  1. Verify the split looks correct")
        print("  2. Configure data.yaml")
        print("  3. Run: python -m yolo.train_model")
    except Exception as e:
        logger.error(f"Failed to split dataset: {e}")
        raise


if __name__ == "__main__":
    main()

