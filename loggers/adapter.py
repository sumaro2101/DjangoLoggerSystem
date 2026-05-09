from pathlib import Path
from collections.abc import Sequence
from typing import Generic, TypeVar, TypeAlias, Protocol, Literal

from logging.handlers import BaseRotatingHandler

RH = TypeVar('RH', bound=BaseRotatingHandler)

LOG_HANDLER: TypeAlias = dict[str, dict[str, str | int]]
LOGGER: TypeAlias = dict[str, dict[str, str | list[str] | bool]]



class RotatingLogger(Protocol, Generic[RH]):

    def __init__(self, logger: type[RH],
                 mb_rotation: int,
                 backup_count: int) -> None:
        ...

    def _get_log_name(self, proj_name: str) -> str:
        ...

    def _set_handler(self, proj_name: str,
                     class_log: type[RH], root_dir: str,
                     mb_rotation: int | None,
                     backup_count: int | None,
                     formatter: str, encoding: str,
                     ) -> LOG_HANDLER:
        ...

    def _set_logger(self, proj_name: str,
                    log_level: Literal['INFO', 'DEBUG', 'WARNING'],
                    *handlers: LOG_HANDLER,
                    propagate: bool,
                    ) -> LOGGER:
        ...

    def __call__(self, proj_name: str,
                 root_dir: Path,
                 formatter: str,
                 encoding: str,
                 log_level: Literal['INFO', 'DEBUG', 'WARNING'],
                 *addition_name_handlers: Sequence[str],
                 mb_rotation: int | None,
                 backup_count: int | None,
                 propagate: bool,
                 ) -> tuple[LOG_HANDLER, LOGGER]:
        ...