import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "app.log")
FMT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"


def setup_logging() -> None:
    os.makedirs(LOG_DIR, exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    if root.handlers:
        return  # already configured (e.g. during reload)

    formatter = logging.Formatter(FMT, datefmt=DATE_FMT)

    # Console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)

    # Rotating file — 10 MB × 5 backups
    fh = RotatingFileHandler(
        LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    root.addHandler(ch)
    root.addHandler(fh)

    # Quiet noisy libs
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
