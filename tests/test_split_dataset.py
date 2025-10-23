import unittest
from pathlib import Path
import shutil
import tempfile
import sys
from yolo.split_dataset import (
    SplitRatios,
    DatasetPaths,
    ImageFileFinder,
    DatasetSplitter,
    create_default_ratios,
    create_dataset_paths,
    parse_arguments,
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
        dataset_name = "test_dataset"
        paths = DatasetPaths(dataset_name)
        expected_root = Path("datasets") / dataset_name
        self.assertEqual(paths.images_source, expected_root / 'images')
        self.assertEqual(paths.labels_source, expected_root / 'labels')
        self.assertEqual(paths.train_images, expected_root / 'train' / 'images')
        self.assertEqual(paths.train_labels, expected_root / 'train' / 'labels')
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
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir)
        self.dataset_name = 'test_dataset'
        self.setup_test_dataset()
    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    def setup_test_dataset(self):
        datasets_dir = Path('datasets') / self.dataset_name
        images_dir = datasets_dir / 'images'
        labels_dir = datasets_dir / 'labels'
        images_dir.mkdir(parents=True, exist_ok=True)
        labels_dir.mkdir(parents=True, exist_ok=True)
        for i in range(10):
            img_file = images_dir / f'image_{i}.jpg'
            lbl_file = labels_dir / f'image_{i}.txt'
            img_file.touch()
            lbl_file.touch()
    def test_splits_dataset_with_default_ratios(self):
        paths = DatasetPaths(self.dataset_name)
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
        paths = DatasetPaths(self.dataset_name)
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        original_count = len(list(paths.images_source.glob('*.jpg')))
        splitter.split()
        remaining_count = len(list(paths.images_source.glob('*.jpg')))
        self.assertEqual(original_count, remaining_count)
    def test_moves_corresponding_labels(self):
        paths = DatasetPaths(self.dataset_name)
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        splitter.split()
        train_images = len(list(paths.train_images.glob('*.jpg')))
        train_labels = len(list(paths.train_labels.glob('*.txt')))
        self.assertEqual(train_images, train_labels)
    def test_clears_existing_split_folders(self):
        paths = DatasetPaths(self.dataset_name)
        paths.train_images.mkdir(parents=True, exist_ok=True)
        existing_file = paths.train_images / 'old_file.jpg'
        existing_file.touch()
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        splitter.split()
        self.assertFalse(existing_file.exists())
    def test_raises_error_when_no_images_found(self):
        empty_dataset = 'empty_dataset'
        empty_dir = Path('datasets') / empty_dataset
        (empty_dir / 'images').mkdir(parents=True)
        (empty_dir / 'labels').mkdir(parents=True)
        paths = DatasetPaths(empty_dataset)
        ratios = SplitRatios()
        splitter = DatasetSplitter(paths, ratios, random_seed=42)
        with self.assertRaises(ValueError):
            splitter.split()
    def test_reproducible_split_with_same_seed(self):
        paths1 = DatasetPaths(self.dataset_name)
        splitter1 = DatasetSplitter(paths1, SplitRatios(), random_seed=42)
        splitter1.split()
        first_train_images = sorted([f.name for f in paths1.train_images.glob('*.jpg')])
        self.tearDown()
        self.setUp()
        paths2 = DatasetPaths(self.dataset_name)
        splitter2 = DatasetSplitter(paths2, SplitRatios(), random_seed=42)
        splitter2.split()
        second_train_images = sorted([f.name for f in paths2.train_images.glob('*.jpg')])
        self.assertEqual(first_train_images, second_train_images)
class FactoryFunctionsTestCase(unittest.TestCase):
    def test_create_default_ratios(self):
        ratios = create_default_ratios()
        self.assertEqual(ratios.train, 0.7)
        self.assertEqual(ratios.val, 0.15)
        self.assertEqual(ratios.test, 0.15)
    def test_create_dataset_paths(self):
        dataset_name = 'test_dataset'
        paths = create_dataset_paths(dataset_name)
        expected_root = Path('datasets') / dataset_name
        self.assertEqual(paths.images_source, expected_root / 'images')
class ParseArgumentsTestCase(unittest.TestCase):
    def test_default_arguments(self):
        sys.argv = ['split_dataset.py']
        args = parse_arguments()
        self.assertEqual(args.dataset, 'image_dataset')
        self.assertEqual(args.seed, 42)
    def test_custom_dataset_argument(self):
        sys.argv = ['split_dataset.py', '--dataset', 'custom_data']
        args = parse_arguments()
        self.assertEqual(args.dataset, 'custom_data')
    def test_custom_seed_argument(self):
        sys.argv = ['split_dataset.py', '--seed', '100']
        args = parse_arguments()
        self.assertEqual(args.seed, 100)
    def test_both_custom_arguments(self):
        sys.argv = ['split_dataset.py', '--dataset', 'my_data', '--seed', '999']
        args = parse_arguments()
        self.assertEqual(args.dataset, 'my_data')
        self.assertEqual(args.seed, 999)
if __name__ == '__main__':
    unittest.main()
class LoggingTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir)
        self.dataset_name = 'test_dataset'
        self.setup_test_dataset()
    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    def setup_test_dataset(self):
        datasets_dir = Path('datasets') / self.dataset_name
        images_dir = datasets_dir / 'images'
        labels_dir = datasets_dir / 'labels'
        images_dir.mkdir(parents=True, exist_ok=True)
        labels_dir.mkdir(parents=True, exist_ok=True)
        for i in range(10):
            img_file = images_dir / f'image_{i}.jpg'
            lbl_file = labels_dir / f'image_{i}.txt'
            img_file.touch()
            lbl_file.touch()
    def test_logs_summary_after_split(self):
        import logging
        with self.assertLogs('yolo.split_dataset', level='INFO') as cm:
            paths = DatasetPaths(self.dataset_name)
            ratios = SplitRatios()
            splitter = DatasetSplitter(paths, ratios, random_seed=42)
            splitter.split()
        log_output = ' '.join(cm.output)
        self.assertIn('Dataset split completed', log_output)
        self.assertIn('Train:', log_output)
        self.assertIn('Val:', log_output)
        self.assertIn('Test:', log_output)
class MainFunctionTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir)
        self.setup_test_dataset()
    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)
    def setup_test_dataset(self):
        datasets_dir = Path('datasets') / 'test_main_dataset'
        images_dir = datasets_dir / 'images'
        labels_dir = datasets_dir / 'labels'
        images_dir.mkdir(parents=True, exist_ok=True)
        labels_dir.mkdir(parents=True, exist_ok=True)
        for i in range(5):
            img_file = images_dir / f'test_{i}.jpg'
            lbl_file = labels_dir / f'test_{i}.txt'
            img_file.touch()
            lbl_file.touch()
    def test_main_function_executes_successfully(self):
        from yolo.split_dataset import main
        from io import StringIO
        sys.argv = ['split_dataset.py', '--dataset', 'test_main_dataset', '--seed', '50']
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
        finally:
            sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        self.assertIn('Dataset split completed successfully', output)
        self.assertIn('Source folders (preserved)', output)
        self.assertIn('Destination folders', output)
    def test_main_function_handles_missing_images_error(self):
        from yolo.split_dataset import main
        sys.argv = ['split_dataset.py', '--dataset', 'nonexistent_dataset']
        with self.assertRaises(FileNotFoundError):
            main()
