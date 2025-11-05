"""
Label Studio integration package for YOLOv11 training.

This package provides tools for annotating images using Label Studio
and converting annotations to YOLO format.

Modules:
    converter: Convert Label Studio JSON exports to YOLO format
    validator: Validate YOLO dataset annotations
    init_dataset: Initialize new dataset structure
"""

__version__ = "1.0.0"
__all__ = ["converter", "validator", "init_dataset"]

