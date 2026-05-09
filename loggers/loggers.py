import os

from logging.handlers import RotatingFileHandler

from .base import BaseRotatingLogger
from .mixins import ZipRotationMixin

LOGLEVEL = os.getenv("DJANGO_LOG_LEVEL", "info").upper()
LOG_ROTATION_MB_VALUE = os.getenv('LOG_ROTATION_MB_VALUE')
LOG_ROTATION_BACKUP_COUNT = int(os.getenv('LOG_ROTATION_BACKUP_COUNT', 5))
LOG_ROTATION_BACKUP_COUNT = LOG_ROTATION_BACKUP_COUNT if LOG_ROTATION_BACKUP_COUNT > 0 else 1
LOG_ROTATION_MB_VALUE = int(LOG_ROTATION_MB_VALUE) * 1024 * 1024 if LOG_ROTATION_MB_VALUE else 5 * 1024 * 1024


class SimpleRotationHandler(BaseRotatingLogger[RotatingFileHandler]):
    ...


class ZipRotationHandler(ZipRotationMixin, SimpleRotationHandler):
    ...

simple_rotation_handler = SimpleRotationHandler(logger=RotatingFileHandler, mb_rotation=LOG_ROTATION_MB_VALUE, backup_count=LOG_ROTATION_BACKUP_COUNT)
zip_rotation_handler = ZipRotationHandler(logger=RotatingFileHandler, mb_rotation=LOG_ROTATION_MB_VALUE, backup_count=LOG_ROTATION_BACKUP_COUNT)
