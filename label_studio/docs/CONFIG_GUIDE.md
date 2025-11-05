# Label Studio Configuration Guide

## Overview

The `label_studio_config.xml` file defines the annotation interface for camera trap images. It supports rich metadata beyond just bounding boxes.

## Configuration File Location

**Path:** `label_studio/label_studio_config.xml`

## Features

### 1. Bounding Box Detection (8 Classes)

Color-coded classes for easy identification:

| Class | Color | Hex Code | Use Case |
|-------|-------|----------|----------|
| bird | Red | #FF6B6B | Any bird species |
| wild_boar | Teal | #4ECDC4 | Wild boars |
| rabbit | Blue | #45B7D1 | Rabbits |
| roe_deer | Green | #96CEB4 | Roe deer |
| fox | Yellow | #FFEAA7 | Foxes |
| human | Gray | #DFE6E9 | Humans (distractor) |
| vehicle | Dark Gray | #636E72 | Vehicles (distractor) |
| unknown_animal | Purple | #A29BFE | Unidentifiable animals |

### 2. Per-Animal Attributes (`perRegion="true"`)

These attributes are **linked to each bounding box individually**, so you can have different values for each animal in the same image:

#### Gender
- male
- female
- unknown_gender

#### Age Class
- juvenile
- adult
- unknown_age

#### Visibility Quality
- clear (animal fully visible, good image)
- partially_occluded (partly hidden by vegetation/objects)
- heavily_occluded (mostly hidden)
- motion_blur (animal moving, blurred)

#### Behavior (Multi-select)
You can select multiple behaviors:
- foraging (eating, searching for food)
- moving (walking, running)
- resting (lying down, standing still)
- alert (looking at camera/threat)
- grooming (cleaning itself)
- interacting (with other animals)

### 3. Image-Level Attributes

These apply to the **entire image**, not individual animals:

#### Time of Day
- day
- night
- dawn_dusk

#### Notes
Free text field for any additional observations about the image.

## How It Works

### Annotation Workflow

1. **Draw bounding box** around an animal
2. **Select class** (bird, wild_boar, etc.)
3. **Set attributes for that animal**:
   - Click on the bounding box
   - Fill in gender, age, visibility, behavior in the sidebar
4. **Repeat** for each animal in the image
5. **Set image-level attributes** (time of day, notes)
6. **Submit**

### Example: Multiple Animals

**Scenario:** Image has 2 wild boars

```
Animal 1 (Box 1):
- Class: wild_boar
- Gender: male
- Age: adult
- Visibility: clear
- Behavior: foraging, alert

Animal 2 (Box 2):
- Class: wild_boar
- Gender: female
- Age: juvenile
- Visibility: partially_occluded
- Behavior: moving

Image-level:
- Time of day: dawn_dusk
- Notes: "Two boars near oak tree, juvenile staying close to mother"
```

## XML Structure Explained

### Key Elements

```xml
<RectangleLabels name="label" toName="image">
```
Defines bounding box tool and available classes.

```xml
<Choices name="gender" toName="image" perRegion="true" ...>
```
- `perRegion="true"` → Links to individual bounding boxes
- `choice="single-radio"` → Only one option can be selected
- `showInline="true"` → Shows horizontally instead of dropdown

```xml
<Choices name="behavior" toName="image" perRegion="true" choice="multiple">
```
- `choice="multiple"` → Can select multiple behaviors

```xml
<Choices name="time_of_day" toName="image" choice="single-radio" ...>
```
- **No** `perRegion="true"` → Applies to entire image

## Customization

### Adding New Classes

Edit `label_studio_config.xml`:

```xml
<RectangleLabels name="label" toName="image">
  <!-- Existing classes... -->
  <Label value="badger" background="#E17055"/>
  <Label value="deer" background="#74B9FF"/>
</RectangleLabels>
```

**Important:** Also update `datasets/DATASET/labels/classes.txt`:
```
bird
wild_boar
rabbit
roe_deer
fox
human
vehicle
unknown_animal
badger
deer
```

### Adding New Attributes

Add a new choice set:

```xml
<!-- After existing Choices -->
<Choices name="health_condition" toName="image" perRegion="true" choice="single-radio">
  <Choice value="healthy"/>
  <Choice value="injured"/>
  <Choice value="unknown"/>
</Choices>
```

### Removing Attributes

Simply delete the `<Choices>` block you don't need. For example, if you don't care about behavior:

```xml
<!-- Remove this entire block:
<Choices name="behavior" toName="image" perRegion="true" choice="multiple">
  <Choice value="foraging"/>
  ...
</Choices>
-->
```

## Exporting Metadata

### Current Implementation

The converter (`label_studio/converter.py`) currently extracts **only bounding boxes**:
- Class name
- Bounding box coordinates (YOLO format)

### Metadata Export (Future Enhancement)

To export metadata attributes, you would need to:

1. Modify `converter.py` to extract metadata from JSON
2. Save to separate files (e.g., `image.json` alongside `image.txt`)
3. Use during training/analysis

**Example JSON export structure:**
```json
{
  "annotations": [
    {
      "result": [
        {
          "type": "rectanglelabels",
          "value": {
            "rectanglelabels": ["wild_boar"],
            "x": 10, "y": 20, "width": 30, "height": 40
          },
          "meta": {
            "gender": ["male"],
            "age_class": ["adult"],
            "visibility": ["clear"],
            "behavior": ["foraging", "alert"]
          }
        }
      ]
    }
  ]
}
```

## Tips for Annotators

### Consistency Guidelines

**Gender:**
- Only mark if clearly visible (visible genitalia, antlers in deer, etc.)
- Use "unknown_gender" when uncertain

**Age:**
- Juvenile: visibly smaller, different proportions, still with mother
- Adult: full size
- Use "unknown_age" if unsure

**Visibility:**
- Clear: >80% of animal visible
- Partially occluded: 40-80% visible
- Heavily occluded: <40% visible
- Motion blur: animal blurred due to movement

**Behavior:**
- Be specific but don't over-analyze
- Multiple behaviors OK (e.g., moving + alert)
- If unsure, leave unchecked

## Testing Configuration

Before starting annotation:

1. Create a test project in Label Studio
2. Import 5-10 sample images
3. Annotate them using all features
4. Export as JSON
5. Check the export format
6. Adjust configuration if needed

## Troubleshooting

### Attributes not showing up?
- Check `perRegion="true"` for per-box attributes
- Save and refresh the page after config changes

### Can't select multiple behaviors?
- Verify `choice="multiple"` in behavior config

### Attributes applying to wrong box?
- Make sure you **click the specific bounding box** before setting attributes
- The selected box is highlighted

### Configuration not saving?
- Click the **Save** button (not just close)
- Check browser console for errors

## References

- [Label Studio XML Tags](https://labelstud.io/tags/)
- [RectangleLabels Documentation](https://labelstud.io/tags/rectanglelabels.html)
- [Choices Documentation](https://labelstud.io/tags/choices.html)

---

**File Location:** `label_studio/label_studio_config.xml`  
**Last Updated:** November 3, 2025  
**Version:** 1.0

