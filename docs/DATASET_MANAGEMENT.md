# Dataset Management - Feature Documentation

## New Features Implemented

### 1. Configurable Dataset Names

Both `create_dataset_structure.py` and `split_dataset.py` now accept custom dataset names via command-line arguments.

**Default behavior:**
```bash
python -m yolo.create_dataset_structure
# Creates: datasets/image_dataset/
```

**Custom dataset name:**
```bash
python -m yolo.create_dataset_structure --dataset animal_detection
# Creates: datasets/animal_detection/
```

### 2. Template-Based README Generation

The README template is now stored in a separate file:
- **Location**: `yolo/templates/datasets/README_TEMPLATE.md`
- **Benefit**: Easy to maintain and update without modifying Python code

### 3. Configurable Random Seed for Splitting

Control the randomness of dataset splits for reproducibility:

```bash
# Default seed (42)
python -m yolo.split_dataset --dataset my_dataset

# Custom seed for different split
python -m yolo.split_dataset --dataset my_dataset --seed 123
```

### 4. Consistent Dataset Root Path

All datasets are created under `datasets/` folder:
```
datasets/
├── animal_dataset/
├── bird_dataset/
├── vehicle_dataset/
└── custom_dataset/
```

## Complete Workflow Examples

### Example 1: Default Dataset

```bash
# Create structure (uses default name: image_dataset)
python -m yolo.create_dataset_structure

# Add images to datasets/image_dataset/images/
# Annotate with labelImg

# Split the dataset
python -m yolo.split_dataset

# Train
python -m yolo.train_model
```

### Example 2: Custom Dataset

```bash
# Create structure with custom name
python -m yolo.create_dataset_structure --dataset wildlife_detection

# Add images to datasets/wildlife_detection/images/
# Annotate: labelImg datasets/wildlife_detection/images datasets/wildlife_detection/labels

# Split with custom seed
python -m yolo.split_dataset --dataset wildlife_detection --seed 100

# Train
python -m yolo.train_model
```

### Example 3: Multiple Datasets

```bash
# Create multiple datasets for different projects
python -m yolo.create_dataset_structure --dataset cats
python -m yolo.create_dataset_structure --dataset dogs
python -m yolo.create_dataset_structure --dataset birds

# Each can be managed independently
python -m yolo.split_dataset --dataset cats
python -m yolo.split_dataset --dataset dogs
python -m yolo.split_dataset --dataset birds
```

## Command-Line Arguments

### create_dataset_structure

```bash
python -m yolo.create_dataset_structure [--dataset DATASET_NAME]
```

**Arguments:**
- `--dataset`: Name of the dataset (default: `image_dataset`)

### split_dataset

```bash
python -m yolo.split_dataset [--dataset DATASET_NAME] [--seed SEED]
```

**Arguments:**
- `--dataset`: Name of the dataset (default: `image_dataset`)
- `--seed`: Random seed for reproducible splits (default: `42`)

## Code Quality Improvements

### Proper Formatting
- ✅ Blank lines between all methods
- ✅ Markdown content extracted to separate template file
- ✅ Clean separation of concerns

### SOLID Principles
- ✅ Single Responsibility: Each class has one clear purpose
- ✅ Dependency Inversion: Uses abstractions (paths, ratios)

### Testing
- ✅ All 13 unit tests pass
- ✅ Tests updated for new parameter-based approach
- ✅ Integration tested with real file operations

## Benefits

1. **Flexibility**: Create and manage multiple datasets for different projects
2. **Reproducibility**: Control random seed for consistent splits
3. **Maintainability**: Template-based approach makes updates easier
4. **Clean Code**: Follows all Python best practices and coding standards
5. **User-Friendly**: Clear command-line interface with helpful defaults

