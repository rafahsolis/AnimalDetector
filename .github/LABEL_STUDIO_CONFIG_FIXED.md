# Label Studio Configuration - Complete ✅

## Summary

Fixed and documented the Label Studio configuration file to properly support rich metadata for camera trap annotation.

## What Was Fixed

### Configuration File Structure

**File:** `label_studio/label_studio_config.xml`

**Key Improvements:**
1. ✅ **Per-animal attributes** properly configured with `perRegion="true"`
   - Gender (male/female/unknown)
   - Age class (juvenile/adult/unknown)
   - Visibility (clear/partially_occluded/heavily_occluded/motion_blur)
   - Behavior (multi-select: foraging, moving, resting, alert, grooming, interacting)

2. ✅ **Image-level attributes** without `perRegion`
   - Time of day (day/night/dawn_dusk)
   - Notes (free text)

3. ✅ **8 color-coded animal classes**
   - bird, wild_boar, rabbit, roe_deer, fox, human, vehicle, unknown_animal

## Documentation Created

### 1. CONFIG_GUIDE.md
**Location:** `label_studio/CONFIG_GUIDE.md`

Complete guide covering:
- Configuration structure explanation
- Per-animal vs image-level attributes
- XML syntax details
- Customization guide (adding classes/attributes)
- Annotation workflow
- Tips for annotators
- Future metadata export considerations

### 2. Updated README.md
**Location:** `label_studio/README.md`

Added:
- Explanation of what the configuration includes
- Reference to CONFIG_GUIDE.md
- Clear distinction between per-animal and image-level attributes

## How It Works

### Per-Animal Attributes (`perRegion="true"`)

When you draw a bounding box, you can set **individual attributes** for that specific animal:

```xml
<Choices name="gender" toName="image" perRegion="true" choice="single-radio">
```

**Example:** Image with 2 wild boars
- Box 1: male, adult, clear, foraging
- Box 2: female, juvenile, partially_occluded, moving

### Image-Level Attributes (no `perRegion`)

These apply to the **entire image**:

```xml
<Choices name="time_of_day" toName="image" choice="single-radio">
```

**Example:** Same image
- Time of day: dawn_dusk
- Notes: "Two boars near oak tree"

## Annotation Workflow

1. Draw bounding box around animal
2. Select class (e.g., wild_boar)
3. Click on the box to select it
4. Fill in attributes in sidebar:
   - Gender: male
   - Age: adult
   - Visibility: clear
   - Behavior: ✓ foraging, ✓ alert
5. Repeat for each animal
6. Set image-level attributes (time of day, notes)
7. Submit

## Current vs Future

### Current Implementation ✅
- **Bounding boxes** → Exported to YOLO format
- **Class labels** → Converted to class IDs
- Rich annotation interface available

### Future Enhancement (Not Yet Implemented)
- **Metadata export** → Would require converter.py modification
- Metadata could be saved alongside YOLO labels
- Useful for:
  - Filtering datasets (e.g., only juveniles)
  - Analysis (behavior patterns)
  - Quality metrics (visibility distribution)

## Files Updated

1. ✅ `label_studio/label_studio_config.xml` - Fixed `perRegion` attributes
2. ✅ `label_studio/CONFIG_GUIDE.md` - Created comprehensive guide
3. ✅ `label_studio/README.md` - Added configuration explanation
4. ✅ `docs/DATASET_MIGRATION.md` - Fixed file path reference

## Example Use Cases

### Basic Annotation
Just draw boxes and select classes → Works perfectly with converter

### Rich Annotation
Draw boxes, select classes, **and** fill in metadata → Captured in Label Studio, available for future export

### Data Analysis
Later you can filter/analyze by:
- "Show me all juvenile wild boars"
- "How many animals were partially occluded?"
- "What behaviors are most common at night?"

## Testing the Configuration

```bash
# 1. Start Label Studio
cd label_studio
docker compose up -d

# 2. Open browser
firefox http://localhost:8080

# 3. Create test project

# 4. Settings → Labeling Interface → Code
# Copy entire contents from label_studio_config.xml

# 5. Import a test image

# 6. Try annotating:
#    - Draw box
#    - Select class
#    - Click box again
#    - Fill attributes in sidebar
#    - Notice how each box can have different attributes!
```

## Benefits

✅ **Rich metadata capture** - Beyond just boxes  
✅ **Per-animal granularity** - Each animal can have different attributes  
✅ **Image-level context** - Time of day, environmental notes  
✅ **Future-proof** - Metadata available for export when needed  
✅ **User-friendly** - Clear color coding, intuitive interface  
✅ **Flexible** - Easy to add/remove attributes

## Documentation Structure

```
label_studio/
├── label_studio_config.xml  # The actual configuration
├── CONFIG_GUIDE.md           # Detailed explanation (NEW)
├── README.md                 # Quick start + workflow
└── docker compose.yml        # Easy startup
```

## Status

**Configuration:** ✅ Fixed and complete  
**Documentation:** ✅ Comprehensive guide created  
**Tested:** ✅ XML structure valid  
**Ready for use:** ✅ Yes

---

**Date:** November 3, 2025  
**Purpose:** Properly configure rich metadata for camera trap annotation  
**Result:** Full-featured annotation interface with per-animal and image-level attributes

