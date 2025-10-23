import unittest
from pathlib import Path
import shutil
import tempfile
from yolo.create_dataset_structure import (
    DatasetStructureCreator,
    parse_arguments,
)
import sys
from io import StringIO


class DatasetStructureCreatorTestCase(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = Path.cwd()
        import os
        os.chdir(self.temp_dir)
        self.dataset_name = 'test_dataset'

    def tearDown(self):
        import os
        os.chdir(self.original_cwd)
        shutil.rmtree(self.temp_dir)

    def test_creates_dataset_root_directory(self):
        creator = DatasetStructureCreator(self.dataset_name)
        creator.create_structure()
        
        dataset_root = Path('datasets') / self.dataset_name
        self.assertTrue(dataset_root.exists())
        self.assertTrue(dataset_root.is_dir())

    def test_creates_images_directory(self):
        creator = DatasetStructureCreator(self.dataset_name)
        creator.create_structure()
        
        images_dir = Path('datasets') / self.dataset_name / 'images'
        self.assertTrue(images_dir.exists())
        self.assertTrue(images_dir.is_dir())

    def test_creates_labels_directory(self):
        creator = DatasetStructureCreator(self.dataset_name)
        creator.create_structure()
        
        labels_dir = Path('datasets') / self.dataset_name / 'labels'
        self.assertTrue(labels_dir.exists())
        self.assertTrue(labels_dir.is_dir())

    def test_creates_readme_file(self):
        creator = DatasetStructureCreator(self.dataset_name)
        creator.create_structure()
        
        readme_file = Path('datasets') / self.dataset_name / 'README.md'
        self.assertTrue(readme_file.exists())
        self.assertTrue(readme_file.is_file())

    def test_readme_contains_dataset_content(self):
        creator = DatasetStructureCreator(self.dataset_name)
        creator.create_structure()
        
        readme_file = Path('datasets') / self.dataset_name / 'README.md'
        content = readme_file.read_text()
        self.assertIn('Animal Detection Dataset', content)
        self.assertIn('Simplified Workflow', content)

    def test_handles_existing_directories(self):
        dataset_root = Path('datasets') / self.dataset_name
        dataset_root.mkdir(parents=True)
        
        creator = DatasetStructureCreator(self.dataset_name)
        creator.create_structure()
        
        self.assertTrue(dataset_root.exists())

    def test_template_path_is_correct(self):
        expected_path = Path('yolo/templates/datasets/README_TEMPLATE.md')
        self.assertEqual(
            DatasetStructureCreator.README_TEMPLATE_PATH.name,
            expected_path.name
        )

    def test_datasets_root_is_correct(self):
        self.assertEqual(
            DatasetStructureCreator.DATASETS_ROOT,
            Path('datasets')
        )

    def test_prints_success_message(self):
        creator = DatasetStructureCreator(self.dataset_name)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        creator.create_structure()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn('Dataset structure created', output)
        self.assertIn(self.dataset_name, output)

    def test_prints_created_directories(self):
        creator = DatasetStructureCreator(self.dataset_name)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        creator.create_structure()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn('Created directories:', output)
        self.assertIn('images', output)
        self.assertIn('labels', output)

    def test_prints_workflow_steps(self):
        creator = DatasetStructureCreator(self.dataset_name)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        creator.create_structure()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn('Simplified Workflow:', output)
        self.assertIn('labelImg', output)
        self.assertIn('split_dataset', output)

    def test_prints_help_message(self):
        creator = DatasetStructureCreator(self.dataset_name)
        
        captured_output = StringIO()
        sys.stdout = captured_output
        creator.create_structure()
        sys.stdout = sys.__stdout__
        
        output = captured_output.getvalue()
        self.assertIn('README.md', output)


class ParseArgumentsTestCase(unittest.TestCase):
    def test_default_dataset_name(self):
        sys.argv = ['create_dataset_structure.py']
        args = parse_arguments()
        self.assertEqual(args.dataset, 'image_dataset')

    def test_custom_dataset_name(self):
        sys.argv = ['create_dataset_structure.py', '--dataset', 'my_dataset']
        args = parse_arguments()
        self.assertEqual(args.dataset, 'my_dataset')


if __name__ == '__main__':
    unittest.main()

