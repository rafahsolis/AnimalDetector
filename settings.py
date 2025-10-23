from pathlib import Path

BASE_DIR = Path(__file__).parent

DEVICE = "0"

MODEL_PATH = "yolov11l.pt"

IMAGE_FOLDER = Path("/mnt/nextcloud/TrailCams")

LOG_FILE = BASE_DIR / "detections.csv"

DATASET_PATH = Path("/mnt/nextcloud/YOLODataset")

TRAINING_EPOCHS = 100

TRAINING_IMAGE_SIZE = 640

MODEL_ARCHITECTURE = "yolov8n.yaml"

TARGET_ANIMALS = [
    "rabbit",
    "fox",
    "wild_boar",
    "bird",
    "deer",
    "cat",
    "dog",
]

DETECTION_CONFIDENCE_THRESHOLD = 0.25

VERBOSE_OUTPUT = False
