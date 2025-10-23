import unittest
from pathlib import Path
import shutil
import tempfile
from yolo.split_dataset import (
    SplitRatios,
    DatasetPaths,
    ImageFileFinder,
    DatasetSplitter,
)


class SplitRatiosTestCase(unittest.TestCase):
    def test_default_ratios_sum_to_one(self):
        ratios = SplitRatios()
        total = ratios.train + ratios.val + ratios.test
        self.assertAlmostEqual(total, 1.0, places=3)

    def test_custom_ratios_are_stored(self):
        ratios = SplitRatios(train=0.8, val=0.1, test=0.1)
        self.assertEqual(ratios.train, 0.8)
        self.assertEqual(ratios.val, 0.1)
        self.assertEqual(ratios.test, 0.1)

    def test_invalid_ratios_raise_error(self):
        with self.assertRaises(ValueError):
            SplitRatios(train=0.5, val=0.3, test=0.3)


class DatasetPathsTestCase(unittest.TestCase):
    def test_paths_are_constructed_correctly(self):
        root = Path("/test/dataset")
        paths = DatasetPaths(root)
        
        self.assertEqual(paths.images_source, root / 'images')
        self.assertEqual(paths.labels_source, root / 'labels')
        self.assertEqual(paths.train_images, root / 'train' / 'images')
        self.assertEqual(paths.train_labels, root / 'train' / 'labels')


class ImageFileFinderTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_finds_supported_image_extensions(self):
        self.create_test_file('image1.jpg')
        self.create_test_file('image2.png')
        self.create_test_file('image3.jpeg')
        
        finder = ImageFileFinder(self.temp_path)
        images = finder.find_all_images()
        
        self.assertEqual(len(images), 3)

    def test_ignores_unsupported_files(self):
        self.create_test_file('image.jpg')
        self.create_test_file('document.txt')
        self.create_test_file('data.json')
        
        finder = ImageFileFinder(self.temp_path)
        images = finder.find_all_images()
        
        self.assertEqual(len(images), 1)

    def test_returns_empty_list_for_nonexistent_folder(self):
        nonexistent = self.temp_path / 'nonexistent'
        finder = ImageFileFinder(nonexistent)
        images = finder.find_all_images()
        
        self.assertEqual(len(images), 0)

    def create_test_file(self, filename: str) -> None:
        file_path = self.temp_path / filename
        file_path.touch()


class DatasetSplitterTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)
        self.setup_test_dataset()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def setup_test_dataset(self):
        images_dir = self.temp_path / 'images'
        labels_dir = self.temp_path / 'labels'
        images_dir.mkdir(exist_ok=True)
        labels_dir.mkdir(exist_ok=True)

        for i in range(10):
            img_file = images_dir / f'image_{i}.jpg'
            lbl_file = labels_dir / f'image_{i}.txt'
            img_file.touch()
            lbl_file.touch()

    def test_splits_dataset_with_default_ratios(self):
        paths = DatasetPaths(self.temp_path)
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        
        splitter.split()
        
        train_count = len(list(paths.train_images.glob('*.jpg')))
        val_count = len(list(paths.val_images.glob('*.jpg')))
        test_count = len(list(paths.test_images.glob('*.jpg')))
        
        self.assertEqual(train_count, 7)
        self.assertEqual(val_count, 1)
        self.assertEqual(test_count, 2)

    def test_copies_files_instead_of_moving(self):
        paths = DatasetPaths(self.temp_path)
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)

        original_count = len(list(paths.images_source.glob('*.jpg')))
        splitter.split()
        remaining_count = len(list(paths.images_source.glob('*.jpg')))

        self.assertEqual(original_count, remaining_count)

    def test_moves_corresponding_labels(self):
        paths = DatasetPaths(self.temp_path)
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        
        splitter.split()
        
        train_images = len(list(paths.train_images.glob('*.jpg')))
        train_labels = len(list(paths.train_labels.glob('*.txt')))
        
        self.assertEqual(train_images, train_labels)

    def test_clears_existing_split_folders(self):
        paths = DatasetPaths(self.temp_path)
        paths.train_images.mkdir(parents=True, exist_ok=True)
        existing_file = paths.train_images / 'old_file.jpg'
        existing_file.touch()
        
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        splitter.split()
        
        self.assertFalse(existing_file.exists())

    def test_raises_error_when_no_images_found(self):
        empty_temp = Path(tempfile.mkdtemp())
        (empty_temp / 'images').mkdir()
        (empty_temp / 'labels').mkdir()
        
        paths = DatasetPaths(empty_temp)
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        
        with self.assertRaises(ValueError):
            splitter.split()
        
        shutil.rmtree(empty_temp)

    def test_reproducible_split_with_same_seed(self):
        self.setup_test_dataset()
        
        paths1 = DatasetPaths(self.temp_path)
        splitter1 = DatasetSplitter(paths1, SplitRatios(), random_seed=42)
        splitter1.split()
        
        first_train_images = sorted([f.name for f in paths1.train_images.glob('*.jpg')])
        
        self.tearDown()
        self.setUp()
        
        paths2 = DatasetPaths(self.temp_path)
        splitter2 = DatasetSplitter(paths2, SplitRatios(), random_seed=42)
        splitter2.split()
        
        second_train_images = sorted([f.name for f in paths2.train_images.glob('*.jpg')])
        
        self.assertEqual(first_train_images, second_train_images)


if __name__ == '__main__':
    unittest.main()

