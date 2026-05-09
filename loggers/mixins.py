from pathlib import Path
from logging.handlers import BaseRotatingHandler

from .rotators import ZipRotatorNamer


class ZipRotationMixin:
    """
    Mixin class that attaches custom ZIP-based log rotation logic to a rotating file handler.

    This mixin monkey-patches the ``namer`` and ``rotator`` attributes of a handler instance
    to use ZIP compression instead of standard text-based rotation. It then delegates
    the remaining handler configuration logic to the parent class.

    Note
    ----
    Intended to be mixed with a subclass of ``logging.handlers.RotatingFileHandler``.
    Ensure ``self._logger`` is initialized and references the handler instance before
    calling ``_set_handler``, as it relies on ``self._logger`` existing.
    """

    def _set_handler(self, proj_name: str,
                    class_log: type[BaseRotatingHandler], root_dir: Path,
                    mb_rotation: int | None,
                    backup_count: int | None,
                    formater: str, encoding: str,
                    ) -> dict[str, dict[str, str | int]]:
        """
        Configure and attach ZIP-based rotation logic, then initialize the log handler.

        Attaches custom ``namer`` and ``rotator`` methods from ``ZipRotatorNamer`` to the
        handler instance, overriding default text-based rotation behavior. Delegates the
        remaining configuration logic to the parent class's ``_set_handler``.

        Parameters
        ----------
        proj_name : str
            Project name used for directory and log file naming.
        class_log : type[BaseRotatingHandler]
            The rotating handler class to instantiate/configure.
        root_dir : Path
            Base directory path where the log directory will be created.
        mb_rotation : int or None
            Maximum log file size in MB. Falls back to instance default if None.
        backup_count : int or None
            Number of backup files to retain. Falls back to instance default if None.
        formatter : str
            Formatter name/class for log messages.
        encoding : str
            Character encoding for the log file.

        Returns
        -------
        dict[str, dict[str, str | int]]
            Handler configuration dictionary as defined by ``LOG_HANDLER``.

        Raises
        ------
        CreateFileError
            If the required directory structure cannot be created by the parent handler.
        AttributeError
            If ``self._logger`` is not properly initialized or lacks expected attributes.
        RuntimeError
            If handler configuration fails unexpectedly.
        """
        self._logger.rotator = ZipRotatorNamer.rotator
        self._logger.namer = ZipRotatorNamer.namer
        return super()._set_handler(proj_name, class_log, root_dir, mb_rotation, backup_count, formater, encoding)
