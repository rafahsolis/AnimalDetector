import unittest
import json
import tempfile
from pathlib import Path
from yolo.label_studio_to_yolo import (
    LabelStudioToYOLOConverter,
    ClassMapper,
    BoundingBoxConverter,
    AnnotationExtractor
)


class TestBoundingBoxConverter(unittest.TestCase):
    def test_label_studio_to_yolo_conversion(self):
        cx, cy, w, h = BoundingBoxConverter.label_studio_to_yolo(
            x=10.0,
            y=20.0,
            width=30.0,
            height=40.0,
            img_width=100,
            img_height=100
        )
        
        self.assertAlmostEqual(cx, 0.25, places=5)
        self.assertAlmostEqual(cy, 0.40, places=5)
        self.assertAlmostEqual(w, 0.30, places=5)
        self.assertAlmostEqual(h, 0.40, places=5)

    def test_validates_coordinates_within_bounds(self):
        result = BoundingBoxConverter.validate_box(0.5, 0.5, 0.3, 0.3)
        self.assertTrue(result)

    def test_rejects_coordinates_out_of_bounds(self):
        result = BoundingBoxConverter.validate_box(1.5, 0.5, 0.3, 0.3)
        self.assertFalse(result)


class TestClassMapper(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.classes_file = Path(self.temp_dir) / 'classes.txt'
        self.create_test_classes_file()

    def create_test_classes_file(self):
        classes = ['bird', 'wild_boar', 'rabbit']
        with open(self.classes_file, 'w') as f:
            for cls in classes:
                f.write(f"{cls}\n")

    def test_loads_classes_from_file(self):
        mapper = ClassMapper(self.classes_file)
        classes = mapper.get_all_classes()
        
        self.assertEqual(len(classes), 3)
        self.assertIn('bird', classes)
        self.assertIn('wild_boar', classes)

    def test_returns_correct_class_id(self):
        mapper = ClassMapper(self.classes_file)
        
        self.assertEqual(mapper.get_class_id('bird'), 0)
        self.assertEqual(mapper.get_class_id('wild_boar'), 1)
        self.assertEqual(mapper.get_class_id('rabbit'), 2)

    def test_raises_error_for_unknown_class(self):
        mapper = ClassMapper(self.classes_file)
        
        with self.assertRaises(ValueError):
            mapper.get_class_id('unknown_animal')


class TestAnnotationExtractor(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.classes_file = Path(self.temp_dir) / 'classes.txt'
        self.create_test_classes_file()
        
        mapper = ClassMapper(self.classes_file)
        self.extractor = AnnotationExtractor(mapper)

    def create_test_classes_file(self):
        classes = ['bird', 'wild_boar']
        with open(self.classes_file, 'w') as f:
            for cls in classes:
                f.write(f"{cls}\n")

    def test_extracts_annotations_from_task(self):
        task = self.create_sample_task()
        yolo_lines = self.extractor.extract_from_task(task)
        
        self.assertEqual(len(yolo_lines), 1)
        self.assertTrue(yolo_lines[0].startswith('0 '))

    def test_returns_empty_for_task_without_annotations(self):
        task = {'data': {}, 'annotations': []}
        yolo_lines = self.extractor.extract_from_task(task)
        
        self.assertEqual(len(yolo_lines), 0)

    def create_sample_task(self):
        return {
            'data': {'image': 'test.jpg'},
            'annotations': [
                {
                    'result': [
                        {
                            'type': 'rectanglelabels',
                            'value': {
                                'rectanglelabels': ['bird'],
                                'x': 10.0,
                                'y': 20.0,
                                'width': 30.0,
                                'height': 40.0
                            },
                            'original_width': 1920,
                            'original_height': 1080
                        }
                    ]
                }
            ]
        }


class TestLabelStudioToYOLOConverter(unittest.TestCase):
    def setUp(self):
        self.temp_dir = Path(tempfile.mkdtemp())
        self.setup_test_environment()

    def setup_test_environment(self):
        self.images_dir = self.temp_dir / 'images'
        self.labels_dir = self.temp_dir / 'labels'
        self.json_export = self.temp_dir / 'export.json'
        self.classes_file = self.labels_dir / 'classes.txt'
        
        self.images_dir.mkdir()
        self.labels_dir.mkdir()
        
        self.create_test_image()
        self.create_classes_file()
        self.create_json_export()

    def create_test_image(self):
        test_image = self.images_dir / 'test.jpg'
        test_image.write_bytes(b'fake image data')

    def create_classes_file(self):
        with open(self.classes_file, 'w') as f:
            f.write('bird\n')
            f.write('wild_boar\n')

    def create_json_export(self):
        export_data = [
            {
                'data': {'image': 'test.jpg'},
                'annotations': [
                    {
                        'result': [
                            {
                                'type': 'rectanglelabels',
                                'value': {
                                    'rectanglelabels': ['bird'],
                                    'x': 10.0,
                                    'y': 20.0,
                                    'width': 30.0,
                                    'height': 40.0
                                },
                                'original_width': 100,
                                'original_height': 100
                            }
                        ]
                    }
                ]
            }
        ]
        
        with open(self.json_export, 'w') as f:
            json.dump(export_data, f)

    def test_creates_label_files(self):
        converter = LabelStudioToYOLOConverter(
            json_export=self.json_export,
            images_dir=self.images_dir,
            labels_dir=self.labels_dir,
            classes_file=self.classes_file,
            skip_duplicates=False
        )
        
        converter.convert()
        
        label_file = self.labels_dir / 'test.txt'
        self.assertTrue(label_file.exists())

    def test_writes_correct_yolo_format(self):
        converter = LabelStudioToYOLOConverter(
            json_export=self.json_export,
            images_dir=self.images_dir,
            labels_dir=self.labels_dir,
            classes_file=self.classes_file,
            skip_duplicates=False
        )
        
        converter.convert()
        
        label_file = self.labels_dir / 'test.txt'
        content = label_file.read_text().strip()
        
        parts = content.split()
        self.assertEqual(len(parts), 5)
        self.assertEqual(parts[0], '0')


if __name__ == '__main__':
    unittest.main()

