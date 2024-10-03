from loguru import logger
from src.core.config import settings

# logger.remove()  # remove sys.stdout

log_levels = settings.logs.levels


def add_file_handler(level: str):
    logger.add(
        settings.logs.path / f"{level.lower()}.log",
        format=settings.logs.format,
        level=level,
        rotation=settings.logs.rotation,
        compression=settings.logs.compression,
        serialize=True,
        delay=True,
        enqueue=True,
        filter=lambda record: record["level"].name == level,
    )


for lvl in log_levels:
    add_file_handler(lvl)


def get_logger(module_name: str):
    return logger.bind(module=module_name)
