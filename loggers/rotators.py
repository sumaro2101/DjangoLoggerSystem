import os
from pathlib import Path
import zipfile

from logging.handlers import BaseRotatingHandler


class ZipRotatorNamer:
    """
    Utility class for compressing rotated log files into ZIP archives and generating archive names.

    Implements the `RotatingFileHandler` interface methods (`rotator` and `namer`) to handle
    post-rotation tasks: zipping the active log file and formatting the resulting archive filename.

    Attributes
    ----------
    FORMAT : str
        The file extension used for archived logs (default: '.zip').
    """
    FORMAT = '.zip'

    @classmethod
    def rotator(cls, source: str | BaseRotatingHandler, dest: str, backupCount: int | None = None) -> None: # noqa: W0613
        """
        Compress a source log file into a ZIP archive and remove the original file.

        Automatically resolves the target file path whether a raw string path or a
        `BaseRotatingHandler` instance is provided. The original file is deleted
        after successful compression.

        Parameters
        ----------
        source : str or BaseRotatingHandler
            The path to the log file or a rotating handler instance.
        dest : str
            The destination path for the resulting ZIP archive.
        backupCount : int or None, optional
            Reserved for API compatibility. Not used in the current implementation.

        Raises
        ------
        FileNotFoundError
            If the source log file does not exist.
        zipfile.BadZipFile
            If the archive cannot be created or written.
        PermissionError
            If insufficient permissions to read, write, or delete files.
        RuntimeError
            If source file removal fails after successful compression.
        """
        source_path = Path(source) if isinstance(source, (str, Path)) else Path(source.baseFilename)
        dest = Path(dest)

        try:
            os.remove(source_path)
        except FileNotFoundError:
            return
        except (PermissionError, OSError) as e:
            raise RuntimeError(f"Failed to remove source log file: {source_path}") from e

        with zipfile.ZipFile(dest, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zipfile.ZIP_DEFLATED) as z_file:
            arcname = source_path.stem
            z_file.write(source_path, arcname)

    @classmethod
    def namer(cls, default_name: str) -> str:
        """
        Generate the archive filename by appending the `.zip` extension.

        Parameters
        ----------
        default_name : str
            The base name of the log file to be archived.

        Returns
        -------
        str
            The formatted filename with the `.zip` extension.
        """
        result = default_name + cls.FORMAT
        return result
