from logging.handlers import RotatingFileHandler

from pathlib import Path

from .adapter import RotatingLogger
from .constants import DEFAULT_BACKUP_COUNT, DEFAULT_MB_ROTATION


class LogRotationFileHandler(RotatingLogger[RotatingFileHandler]):

    def __init__(self, logger, mb_rotation = DEFAULT_MB_ROTATION, backup_count = DEFAULT_BACKUP_COUNT):
        self._logger = logger
        self._mb_rotation = mb_rotation
        self._backup_count = backup_count

    def _get_log_name(self, proj_name):
        return proj_name + '_file'

    def _set_handler(self, proj_name, class_log, root_dir, mb_rotation, backup_count, formatter = 'simple', encoding = 'utf-8'):
        file_name = proj_name + '.log'
        root_dir = root_dir.joinpath(proj_name)
        root_dir.mkdir(parents=True, exist_ok=True)
        return {
            self.get_log_name(proj_name):
                {
                    'class': class_log,
                    'filename': str(root_dir.joinpath(file_name)),
                    'formatter': formatter,
                    'maxBytes': self._mb_rotation if not mb_rotation else mb_rotation,
                    'backupCount': self._backup_count if not backup_count else backup_count,
                    'encoding': encoding,
                    },
                }

    def _set_logger(self, proj_name, log_level, *handlers, propagate = False):
        return {
            proj_name:
                {
                    'level': log_level,
                    'handlers': list(handlers),
                    'propagate': propagate,
                    }
                }

    def __call__(self, proj_name, root_dir, formatter = 'simple', encoding = 'utf-8', log_level = 'INFO', *addition_name_handlers, mb_rotation = None, backup_count = None, propagate = False):
        log_handler = self._set_handler(proj_name, self._logger, root_dir, mb_rotation, backup_count, formatter, encoding)
        logger = self._set_logger(proj_name, log_level.upper(), self._get_log_name(proj_name), *addition_name_handlers)
        return (log_handler, logger)
