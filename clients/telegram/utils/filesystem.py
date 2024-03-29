import time
from pathlib import Path
from utils.string import join_by


def check_file(path: str):
    file = Path(path)

    if not file.exists():
        raise FileExistsError(f'File does not exists: {path}')

    if not file.is_file():
        raise ValueError(f'Not a file: {path}')


def check_folder(path: str):
    folder = Path(path)

    if not folder.exists():
        raise FileExistsError(f'File does not exists: {path}')

    if not folder.is_dir():
        raise ValueError(f'Not a folder: {path}')


def read(path: str, mode: str = 'r', encoding: str = None):
    check_file(path)
    with open(path, mode, encoding=encoding) as f:
        return f.read()


def write(path: str, data: bytes | str, mode: str = 'w', encoding: str = None):
    with open(path, mode, encoding=encoding) as f:
        return f.write(data)


def iter_files(folder):
    check_folder(folder)

    return Path(folder).iterdir()


def safe_filename(ext: str, prefix: str = '') -> str:
    return prefix + join_by(str(time.time()), ext)
