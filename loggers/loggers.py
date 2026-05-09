from logging.handlers import RotatingFileHandler

from .base import BaseRotatingLogger
from .mixins import ZipRotationMixin


class SimpleRotationHandler(BaseRotatingLogger[RotatingFileHandler]):
    ...


class ZipRotationHandler(ZipRotationMixin, SimpleRotationHandler):
    ...
