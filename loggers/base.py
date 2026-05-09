from pathlib import Path
from collections.abc import Sequence
from typing import Generic, TypeVar, TypeAlias, Protocol, Literal

from logging.handlers import BaseRotatingHandler
from .exeptions import CreateFileError

RH = TypeVar('RH', bound=BaseRotatingHandler)

LOG_HANDLER: TypeAlias = dict[str, dict[str, str | int]]
LOGGER: TypeAlias = dict[str, dict[str, str | list[str] | bool]]



class BaseRotatingLogger(Protocol, Generic[RH]):
    """
    A protocol class defining the interface for configuring rotating log handlers and loggers.

    This protocol specifies how to instantiate and configure rotating log handlers and their parent loggers.
    It is designed to be generic over a specific rotating handler type (RH) and returns configuration dictionaries
    rather than instantiated objects, allowing for further processing or integration into a logging framework.

    Parameters
    ----------
    logger : type[RH]
        The rotating handler class to be used for log output.
    mb_rotation : int
        The maximum size of log files in megabytes before rotation occurs.
    backup_count : int
        The number of rotated log files to keep.
    """
    def __init__(self, logger: type[RH],
                 mb_rotation: int,
                 backup_count: int) -> None:
        """
        Initialize the protocol instance with default rotation parameters.

        Parameters
        ----------
        logger : type[RH]
            The rotating handler class to be used.
        mb_rotation : int
            Default maximum log file size in MB.
        backup_count : int
            Default number of backup files to retain.
        """
        self._logger = logger
        self._mb_rotation = mb_rotation
        self._backup_count = backup_count

    def _get_log_name(self, proj_name: str) -> str:
        """
        Generate a base name for the log file.

        Appends '_file' to the provided project name to create a standardized log filename.

        Parameters
        ----------
        proj_name : str
            The name of the project.

        Returns
        -------
        str
            The generated base log filename.
        """
        return proj_name + '_file'

    def _set_handler(self, proj_name: str,
                     class_log: type[RH], root_dir: Path,
                     mb_rotation: int | None,
                     backup_count: int | None,
                     formatter: str, encoding: str,
                     ) -> LOG_HANDLER:
        """
        Configure and return a dictionary describing a rotating log handler.

        Creates the necessary directory structure and returns a configuration dictionary
        containing parameters for initializing a rotating log handler.

        Parameters
        ----------
        proj_name : str
            The project name used for directory and log file naming.
        class_log : type[RH]
            The rotating handler class to configure.
        root_dir : Path
            The base directory path where the log directory will be created.
        mb_rotation : int or None
            Maximum log file size in MB. Falls back to instance default if None.
        backup_count : int or None
            Number of backup files to keep. Falls back to instance default if None.
        formatter : str
            The formatter name or class to use for log messages.
        encoding : str
            The character encoding for the log file.

        Returns
        -------
        LOG_HANDLER
            A dictionary containing handler configuration parameters.

        Raises
        ------
        CreateFileError
            If the required directory cannot be created.
        """
        file_name = proj_name + '.log'
        root_dir = root_dir.joinpath(proj_name)
        try:
            root_dir.mkdir(parents=True, exist_ok=True)
        except FileNotFoundError:
            raise CreateFileError(f'Can`t create file - "{str(root_dir)}".')
        return {
            self._get_log_name(proj_name):
                {
                    'class': class_log,
                    'filename': str(root_dir.joinpath(file_name)),
                    'formatter': formatter,
                    'maxBytes': self._mb_rotation if not mb_rotation else mb_rotation,
                    'backupCount': self._backup_count if not backup_count else backup_count,
                    'encoding': encoding,
                    },
                }

    def _set_logger(self, proj_name: str,
                    *handlers: Sequence[str],
                    log_level: Literal['INFO', 'DEBUG', 'WARNING'],
                    propagate: bool,
                    ) -> LOGGER:
        """
        Configure and return a dictionary describing a logger.

        Returns a configuration dictionary containing the logger's level, associated handlers,
        and propagation settings.

        Parameters
        ----------
        proj_name : str
            The name of the logger.
        *handlers : Sequence[str]
            Configuration names for the handlers to attach to this logger.
        log_level : Literal['INFO', 'DEBUG', 'WARNING']
            The minimum logging level to record.
        propagate : bool
            Whether log messages should propagate to parent loggers.

        Returns
        -------
        LOGGER
            A dictionary containing logger configuration parameters.
        """
        return {
            proj_name:
                {
                    'level': log_level,
                    'handlers': list(handlers),
                    'propagate': propagate,
                    }
                }

    def __call__(self, proj_name: str,
                 root_dir: Path,
                 *addition_name_handlers: Sequence[str],
                 formatter: str = 'simple',
                 encoding: str = 'utf-8',
                 log_level: Literal['INFO', 'DEBUG', 'WARNING'] = 'INFO',
                 mb_rotation: int | None = None,
                 backup_count: int | None = None,
                 propagate: bool = False,
                 ) -> tuple[LOG_HANDLER, LOGGER]:
        """
        Configure and return dictionaries for both a rotating log handler and its logger.

        This method orchestrates the setup process by delegating to internal configuration methods.
        It returns a tuple containing the handler configuration and the logger configuration.

        Parameters
        ----------
        proj_name : str
            The project name for naming logs and directories.
        root_dir : Path
            The base directory path for log storage.
        *addition_name_handlers : Sequence[str]
            Additional handler names to be attached to the logger.
        formatter : str, default 'simple'
            The formatter to use for log messages.
        encoding : str, default 'utf-8'
            The character encoding for log files.
        log_level : Literal['INFO', 'DEBUG', 'WARNING'], default 'INFO'
            The minimum logging level.
        mb_rotation : int or None, default None
            Maximum log file size in MB.
        backup_count : int or None, default None
            Number of backup files to retain.
        propagate : bool, default False
            Whether log messages should propagate to parent loggers.

        Returns
        -------
        tuple[LOG_HANDLER, LOGGER]
            A tuple containing the handler configuration dictionary and the logger configuration dictionary.
        """
        log_handler = self._set_handler(proj_name, self._logger,
                                        root_dir, mb_rotation, backup_count,
                                        formatter, encoding)
        logger = self._set_logger(proj_name,
                                  self._get_log_name(proj_name), *addition_name_handlers,
                                  log_level=log_level.upper(), propagate=propagate)
        return (log_handler, logger)
