# Label Studio Command Migration Guide

## What Changed?

Label Studio tools have been moved to their own dedicated package for better organization.

## Quick Command Reference

### Old Commands → New Commands

| Old Command | New Command |
|-------------|-------------|
| `python -m yolo.label_studio_to_yolo` | `python -m label_studio.converter` |
| `python -m yolo.validate_annotations` | `python -m label_studio.validator` |
| `python -m yolo.init_dataset` | `python -m label_studio.init_dataset` |

### Commands That Didn't Change

These remain in the `yolo` package:
- `python -m yolo.split_dataset`
- `python -m yolo.generate_data_yaml`
- `python -m yolo.train_model`

## Examples

### Before (Old)

```bash
# Initialize dataset
python -m yolo.init_dataset fototrampeo_bosque

# Convert annotations
python -m yolo.label_studio_to_yolo \
    --json export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt

# Validate
python -m yolo.validate_annotations \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

### After (New)

```bash
# Initialize dataset
python -m label_studio.init_dataset fototrampeo_bosque

# Convert annotations
python -m label_studio.converter \
    --json export.json \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt

# Validate
python -m label_studio.validator \
    --images datasets/fototrampeo_bosque/images \
    --labels datasets/fototrampeo_bosque/labels \
    --classes datasets/fototrampeo_bosque/labels/classes.txt
```

## Why the Change?

### Better Organization
- All Label Studio tools in one place: `label_studio/`
- YOLO training tools stay in `yolo/`
- Clear separation of concerns

### Clearer Names
- `converter.py` is more intuitive than `label_studio_to_yolo.py`
- `validator.py` is clearer than `validate_annotations.py`

### Future-Proof
- Easier to add new Label Studio features
- Can import as module: `from label_studio import converter`

## Shell Aliases (Optional)

If you prefer shorter commands, add these to your `~/.bashrc` or `~/.zshrc`:

```bash
# Label Studio shortcuts
alias ls-init='python -m label_studio.init_dataset'
alias ls-convert='python -m label_studio.converter'
alias ls-validate='python -m label_studio.validator'

# YOLO shortcuts
alias yolo-split='python -m yolo.split_dataset'
alias yolo-yaml='python -m yolo.generate_data_yaml'
alias yolo-train='python -m yolo.train_model'
```

Then use:
```bash
ls-init my_dataset
ls-convert --json export.json --images ... --labels ... --classes ...
ls-validate --images ... --labels ... --classes ...
yolo-split --dataset my_dataset
yolo-yaml --dataset my_dataset
yolo-train
```

## Need Help?

All documentation has been updated to use the new commands:
- `docs/LABEL_STUDIO_GUIDE.md` - Complete workflow guide
- `docs/LABEL_STUDIO_QUICK_REF.md` - Quick command reference
- `docs/README_LABEL_STUDIO.md` - Package overview

## Backward Compatibility

**Important:** The old commands no longer exist. Update any scripts or documentation you have to use the new commands.

If you have scripts using the old commands, use find/replace:
```bash
# In your scripts, replace:
yolo.label_studio_to_yolo    → label_studio.converter
yolo.validate_annotations     → label_studio.validator
yolo.init_dataset            → label_studio.init_dataset
```

---

**Migration Date:** November 3, 2025  
**Status:** Complete ✓

