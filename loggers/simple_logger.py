from typing import ClassVar
from logging.handlers import RotatingFileHandler, BaseRotatingHandler

from pathlib import Path
from .rotators import ZipRotatorNamer


class LogRotationFileHandler:
    """
    Класс для создания адаптивных обработчиков логов с сохранением и
    ротацией в файлы.

    Attributes
    ----------
    class_log : str
        Какой класс используется для обработки.
    MB_ROTATION : int
        Количество мегабайт для ротации.
    BACKUP_COUNT : int
        Количество ротаций.

    Methods
    -------
    get_log_name(proj_name='some_name')
        Выводит имя лога.

    set_handler(proj_name='some_name', root_dit=Path('logs'), formater: 'simple')
        Устанавливает обработчик согласно имени проекта.

    set_logger(proj_name='some_name, log_level: 'INFO', 'handle_1', 'handle_1')
        Устанавлиет логгер.

    Examples
    --------
    >>> LogRotationFileHandler.set_handler('some_name', Path('logs'), 'simple')
    {
        some_name_file: {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/some_name.log',
            'formatter': 'simple',
            'maxBytes': 5242880,
            'backupCount': 5,
            'encoding': 'utf8',
        }
    }
    """
    class_log: ClassVar[type[BaseRotatingHandler]] = RotatingFileHandler
    MB_ROTATION: ClassVar[int] = 5 * 1024 * 1024
    BACKUP_COUNT: ClassVar[int] = 5

    @classmethod
    def get_log_name(cls, proj_name: str) -> str:
        """
        Вывод имени файла логов.

        Parameters
        ----------
        proj_name : str
            Имя.

        Returns
        -------
        str
            Имя файла логов.
        """
        return proj_name + '_file'

    @classmethod
    def set_handler(cls, proj_name: str,
                    root_dir: Path,
                    formater: str, encoding: str = 'utf8',
                    ) -> dict[str, dict[str, str | int]]:
        """
        Установка обработчика с настройками.

        Parameters
        ----------
        proj_name : str
            Имя.
        root_dir : Path
            Корневая папка для сохранения.
        formater : str
            Используемый формат.
        encoding : str, optional
            Кодирование, by default 'utf8'

        Returns
        -------
        dict[str, dict[str, str | int]]
            Обработчик с конфигурацией.

        Examples
        --------
        >>> LogRotationFileHandler.set_handler('some_name', Path('logs'), 'simple')
        {
            some_name_file: {
                'class': 'RotatingFileHandler',
                'filename': 'logs/some_name/some_name.log',
                'formatter': 'simple',
                'maxBytes': 5242880,
                'backupCount': 5,
                'encoding': 'utf8',
            }
        }
        """
        file_name = proj_name + '.log'
        root_dir = root_dir.joinpath(proj_name)
        root_dir.mkdir(parents=True, exist_ok=True)
        return {
            cls.get_log_name(proj_name):
                {
                    'class': cls.class_log,
                    'filename': str(root_dir.joinpath(file_name)),
                    'formatter': formater,
                    'maxBytes': cls.MB_ROTATION,
                    'backupCount': cls.BACKUP_COUNT,
                    'encoding': encoding,
                    },
                }

    @classmethod
    def set_logger[*T](cls, proj_name: str,
                       log_level: str,
                       *handlers: *T, propagate: bool = False,
                       ) -> dict[str, dict[str, (str | list[str] | bool)]]:
        """
        Установка логов с настройками.

        Parameters
        ----------
        proj_name : str
            Имя.
        log_level : str
            Уровень логирования.
        handlers : *T
            Имена обработчиков.
        propagate : bool, optional
            Распространение, by default False

        Returns
        -------
        dict[str[dict[str, list[str], bool]]]
            Лог с настройками
        """
        return {
            proj_name:
                {
                    'level': log_level,
                    'handlers': list(handlers),
                    'propagate': propagate,
                    }
                }


class LogZipRotationFileHandler(LogRotationFileHandler):

    @classmethod
    def set_handler(cls, proj_name: str,
                    root_dir: Path,
                    formater: str, encoding: str = 'utf8',
                    ) -> dict[str, dict[str, str | int]]:
        cls.class_log.rotator = ZipRotatorNamer.rotator
        cls.class_log.namer = ZipRotatorNamer.namer
        return super().set_handler(proj_name, root_dir, formater, encoding)
