# Animal Detection Dataset
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
6. **Run training** using yolo/train_model.py
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
