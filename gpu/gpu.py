import torch
from simple_settings import settings
from logger.config import get_logger

logger = get_logger('gpu')


def log_gpu_status_header() -> None:
    header = f"{'=' * 50}\nGPU Configuration Check\n{'=' * 50}"
    logger.info(header)


def check_gpu_availability() -> bool:
    is_available = torch.cuda.is_available()
    if settings.VERBOSE_OUTPUT:
        _log_pytorch_version()
        _log_cuda_status(is_available)
    return is_available


def _log_pytorch_version() -> None:
    logger.info(f"PyTorch version: {torch.__version__}")


def _log_cuda_status(is_available: bool) -> None:
    logger.info(f"CUDA available: {is_available}")
    if is_available:
        _log_cuda_info()
    else:
        _log_cuda_warning()


def _log_cuda_info() -> None:
    memory_mb = torch.cuda.memory_allocated(0) / 1024**2
    cuda_info = (
        f"CUDA version: {torch.version.cuda}\n"
        f"GPU count: {torch.cuda.device_count()}\n"
        f"GPU name: {torch.cuda.get_device_name(0)}\n"
        f"Current GPU memory allocated: {memory_mb:.2f} MB"
    )
    logger.info(cuda_info)


def _log_cuda_warning() -> None:
    logger.warning("CUDA not available. Running on CPU.")


def get_device_name(device: str) -> str:
    if device == '0':
        return 'GPU (cuda:0)'
    return 'CPU'

