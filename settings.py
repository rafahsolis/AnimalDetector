from pathlib import Path


VERBOSE_OUTPUT = True
DEVICE = '0'
IMAGE_FOLDER = Path('images')
MODELS_DIR = Path('yolo/models')
MODEL_PATH = MODELS_DIR / 'yolov8n.pt'
LOG_FILE = Path('results.csv')
DETECTION_CONFIDENCE_THRESHOLD = 0.25
TARGET_ANIMALS = ["rabbit", "fox", "wild_boar", "bird"]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'simple': {
            'format': '%(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'level': 'INFO',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'logs/animal_detector.log',
            'formatter': 'verbose',
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG',
    },
    'loggers': {
        'yolo': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'main': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

