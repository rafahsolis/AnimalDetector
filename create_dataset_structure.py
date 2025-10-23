from pathlib import Path
class DatasetStructureCreator:
    def __init__(self, dataset_root: Path) -> None:
        self._dataset_root = dataset_root
    def create_structure(self) -> None:
        self._create_root_directory()
        self._create_split_directories()
        self._create_readme()
        self._log_completion()
    def _create_root_directory(self) -> None:
        self._dataset_root.mkdir(parents=True, exist_ok=True)
    def _create_split_directories(self) -> None:
        splits = ['train', 'val', 'test']
        for split in splits:
            self._create_split_subdirectories(split)
    def _create_split_subdirectories(self, split: str) -> None:
        split_path = self._dataset_root / split
        images_path = split_path / 'images'
        labels_path = split_path / 'labels'
        images_path.mkdir(parents=True, exist_ok=True)
        labels_path.mkdir(parents=True, exist_ok=True)
    def _create_readme(self) -> None:
        readme_path = self._dataset_root / 'README.md'
        content = self._get_readme_content()
        readme_path.write_text(content)
    def _get_readme_content(self) -> str:
        return """# Animal Detection Dataset
## Structure
This dataset follows the YOLO format:
\`\`\`
animal_dataset/
├── data.yaml              # Configuration file (copy from data.yaml.example)
├── train/
│   ├── images/           # Put 70-80% of your images here
│   └── labels/           # Corresponding label files
├── val/
│   ├── images/           # Put 10-15% of your images here
│   └── labels/           # Corresponding label files
└── test/
    ├── images/           # Put 10-15% of your images here
    └── labels/           # Corresponding label files
\`\`\`
## Next Steps
1. **Copy and rename** \`data.yaml.example\` to \`data.yaml\`
2. **Edit** \`data.yaml\` to match your absolute paths
3. **Add images** to train/images/, val/images/, test/images/
4. **Add labels** to train/labels/, val/labels/, test/labels/
   - Each image needs a matching label file (same name, .txt extension)
5. **Verify** that class IDs in labels match those in data.yaml
6. **Run training** using train_model.py
## Label Format
Each label file is a text file with one line per object:
\`\`\`
<class_id> <x_center> <y_center> <width> <height>
\`\`\`
Example (rabbit in center of image):
\`\`\`
0 0.5 0.5 0.2 0.3
\`\`\`
See label_format_example.txt for more details.
## Annotation Tools
Use one of these to create labels:
- **LabelImg**: \`pip install labelImg\` then run \`labelImg\`
- **Roboflow**: https://roboflow.com (web-based)
- **CVAT**: https://www.cvat.ai (advanced)
Make sure to select YOLO format when exporting!
"""
    def _log_completion(self) -> None:
        print(f"✓ Dataset structure created at: {self._dataset_root}")
        print("\nCreated directories:")
        print(f"  - {self._dataset_root / 'train' / 'images'}")
        print(f"  - {self._dataset_root / 'train' / 'labels'}")
        print(f"  - {self._dataset_root / 'val' / 'images'}")
        print(f"  - {self._dataset_root / 'val' / 'labels'}")
        print(f"  - {self._dataset_root / 'test' / 'images'}")
        print(f"  - {self._dataset_root / 'test' / 'labels'}")
        print("\nNext steps:")
        print("  1. Copy data.yaml.example to data.yaml")
        print("  2. Edit data.yaml with your absolute paths")
        print("  3. Add annotated images and labels")
        print("  4. Run: python train_model.py")
def main() -> None:
    dataset_root = Path("datasets/animal_dataset")
    creator = DatasetStructureCreator(dataset_root)
    creator.create_structure()
if __name__ == "__main__":
    main()
