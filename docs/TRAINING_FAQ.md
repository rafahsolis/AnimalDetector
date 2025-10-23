# Training FAQ - Frequently Asked Questions
## General Questions
### Q: How many images do I need?
**A:** Minimum 100-300 per animal class, but more is always better:
- **100-300 images**: Basic model, may work for simple scenarios
- **500-1000 images**: Good model, reliable performance
- **1000+ images**: Excellent model, production-ready
### Q: How long does training take?
**A:** Depends on your hardware and dataset:
- **GPU (NVIDIA RTX 3060)**: 2-4 hours for 100 epochs with 1000 images
- **GPU (NVIDIA RTX 4090)**: 1-2 hours for 100 epochs with 1000 images
- **CPU**: 1-3 days (not recommended)
### Q: Do I need a GPU?
**A:** Highly recommended but not required:
- **With GPU**: Training is 50-100x faster
- **Without GPU**: Will work but very slow, use fewer epochs and smaller model
### Q: Which YOLO model should I start with?
**A:** Start with **yolo11n.pt** for fast experimentation:
- `yolo11n.pt`: Fastest, good for testing
- `yolo11m.pt`: Balanced, recommended for production
- `yolo11l.pt`: Best accuracy, slower
You can always retrain with a larger model later.
## Dataset Questions
### Q: What image format should I use?
**A:** JPG or PNG are both fine. YOLO handles both automatically.
### Q: What image size/resolution?
**A:** Any size works, but consider:
- **Minimum**: 640x640 pixels
- **Recommended**: 1920x1080 or higher
- **Maximum**: No limit, but larger images slow down training
YOLO automatically resizes images during training.
### Q: Should all images be the same size?
**A:** No! YOLO handles different sizes automatically. Mix of sizes is actually beneficial.
### Q: Can I use images from the internet?
**A:** Yes, but:
- Ensure you have rights to use them
- More variety = better model
- Try to match your real-world use case
### Q: How do I split train/val/test datasets?
**A:** Typical split:
- **70%** training
- **15%** validation
- **15%** testing
Randomly distribute images, don't put all similar images in one split.
### Q: My dataset is unbalanced (more rabbits than foxes), is that okay?
**A:** It can work, but try to balance it:
- **Ideal**: Equal number of images per class
- **Acceptable**: 2:1 ratio maximum
- **Problematic**: 10:1 ratio, model may ignore minority class
## Annotation Questions
### Q: How precise do my bounding boxes need to be?
**A:** Reasonably precise:
- Box should tightly fit the animal
- Small gaps are okay
- Don't need pixel-perfect precision
- Consistency is more important than perfection
### Q: Should I annotate partially visible animals?
**A:** Yes! Include:
- Animals partially hidden by objects
- Animals at image edges
- Partially occluded animals
This helps the model learn to detect animals in real-world scenarios.
### Q: What if an animal is very small in the image?
**A:** Annotate it anyway if you want to detect small animals. If not interested in small/distant animals, skip them.
### Q: Can I have multiple animals in one image?
**A:** Absolutely! This is normal and encouraged. Just create multiple bounding boxes in the same label file.
### Q: I made a mistake in annotation, how do I fix it?
**A:** Simply re-annotate using LabelImg:
1. Open the image
2. Delete wrong box (select and press Delete)
3. Draw new box
4. Save
## Training Questions
### Q: Training stopped with "CUDA out of memory", what do I do?
**A:** Reduce memory usage:
```python
# In train_model.py, reduce batch_size
batch_size = 8  # Try 8, 4, or even 1
```
Or use a smaller model (yolo11n instead of yolo11l).
### Q: How do I know if training is going well?
**A:** Watch the losses in terminal output:
- **Good**: Losses decrease steadily
- **Bad**: Losses stay constant or increase
- **Normal**: Some fluctuation is expected
Check `runs/detect/train/results.png` for visualization.
### Q: Should I use all 100 epochs?
**A:** Not necessarily:
- Training auto-stops if no improvement (patience parameter)
- Check validation metrics, if they plateau, you can stop
- More epochs ≠ always better (risk of overfitting)
### Q: What's overfitting and how do I avoid it?
**A:** Overfitting = model memorizes training data but fails on new images.
**Signs:**
- Training loss very low, but validation loss high
- Great on training images, poor on new images
**Solutions:**
- More training data
- Data augmentation (YOLO does this automatically)
- Fewer epochs
- Regularization (dropout, already in YOLO)
### Q: Can I resume training if it stops?
**A:** Yes! YOLO saves checkpoints. Modify train_model.py:
```python
# Load the last checkpoint
model_path = Path("runs/detect/train/weights/last.pt")
```
### Q: Can I train on multiple GPUs?
**A:** Yes, modify device parameter:
```python
device = "0,1"  # Use GPU 0 and 1
```
## Results Questions
### Q: What's a good mAP score?
**A:**
- **mAP50 > 0.7**: Good, usable model
- **mAP50 > 0.8**: Very good
- **mAP50 > 0.9**: Excellent
Context matters - depends on your use case.
### Q: My model detects animals but wrong species, why?
**A:** Common causes:
- Not enough training data
- Similar-looking animals (fox vs dog)
- Wrong class IDs in label files
- Need more training epochs
**Solution:** Add more diverse training examples of each species.
### Q: Model works on training images but not new images, why?
**A:** Likely overfitting or data mismatch:
- Training images don't represent real-world scenarios
- Need more variety in training data
- Different lighting/angles in real images
### Q: How do I improve accuracy?
**A:** Several approaches:
1. **More data**: Most effective solution
2. **Better data**: More variety, better annotations
3. **Larger model**: yolo11m or yolo11l instead of yolo11n
4. **More epochs**: If losses still decreasing
5. **Higher image size**: 1280 instead of 640
6. **Clean data**: Remove bad annotations
## Technical Questions
### Q: What does each training parameter do?
**epochs**: How many times model sees all training data
- More = better learning (to a point)
- Typical: 50-300
**image_size**: Input image dimensions (640, 1280, etc.)
- Larger = better accuracy, slower training
- Must be multiple of 32
**batch_size**: Images processed together
- Larger = faster training, more GPU memory
- Smaller = slower, less memory
- Typical: 8, 16, 32
**confidence_threshold**: Minimum confidence to accept detection (0.0-1.0)
- Lower = more detections (more false positives)
- Higher = fewer detections (more missed animals)
- Typical: 0.25
### Q: Where are training results saved?
**A:** `runs/detect/train/` directory:
- `weights/best.pt`: Best model
- `weights/last.pt`: Last epoch
- `results.png`: Training curves
- `confusion_matrix.png`: Classification accuracy
- `val_batch0_pred.jpg`: Example predictions
### Q: Can I delete runs/detect/train/ folders?
**A:** Yes, but save your `best.pt` first! Copy it somewhere safe before deleting.
### Q: How do I use my trained model?
**A:** Update settings:
```python
# settings_local.py
MODEL_PATH = Path('runs/detect/train/weights/best.pt')
```
Then run: `python main.py`
## Troubleshooting
### Q: Error: "No labels found in dataset"
**A:** Check:
1. Labels folder exists: `train/labels/`, `val/labels/`
2. Label files match image names: `img001.jpg` → `img001.txt`
3. Path in data.yaml is correct (use absolute path)
4. Label files are not empty
### Q: Error: "Dataset not found"
**A:** Check data.yaml:
- Use absolute path for `path:` field
- Verify train/val/test paths are correct
- Check folders actually exist
### Q: Error: "Invalid YOLO format"
**A:** Check label files:
- 5 values per line: `class_id x_center y_center width height`
- Values space-separated (not comma)
- Coordinates between 0.0 and 1.0
- No extra whitespace
### Q: Training is very slow
**A:** Solutions:
- Ensure GPU is being used (check DEVICE setting)
- Use smaller model (yolo11n)
- Reduce image_size to 640
- Reduce batch_size (won't speed up but reduces memory)
### Q: Model detects everything as one class
**A:** Check:
- Class IDs in labels match data.yaml
- Have examples of all classes
- Classes are visually distinct
- Need more training data/epochs
## Best Practices
### Do's ✓
- Start with a small dataset (50 images) to test workflow
- Use diverse images (different angles, lighting, backgrounds)
- Annotate consistently
- Validate dataset before training
- Monitor training metrics
- Keep best.pt model safe
- Test on completely new images
### Don'ts ✗
- Don't train without validating dataset first
- Don't use only similar images
- Don't ignore validation metrics
- Don't delete runs/detect/ without saving best.pt
- Don't expect perfection with small dataset
- Don't train on CPU for large datasets
- Don't use untested models in production
## Getting Help
If you're still stuck:
1. **Check logs**: `logs/animal_detector.log`
2. **Validate dataset**: `python validate_dataset.py`
3. **Review training output**: Look for error messages
4. **Check documentation**: `docs/TRAINING_GUIDE.md`
5. **Verify structure**: Ensure folders match required format
## Quick Reference
**Minimum viable dataset:**
```
- 100 images per class
- 640x640 pixel resolution
- Proper YOLO label format
- 70/15/15 train/val/test split
```
**Quick training command:**
```bash
python create_dataset_structure.py  # Setup
labelImg                            # Annotate
python validate_dataset.py          # Verify
python train_model.py               # Train
```
**After training:**
```bash
# View results
ls runs/detect/train/
# Use model
# Edit settings_local.py, then:
python main.py
```
