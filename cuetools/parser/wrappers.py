from typing import IO, Iterator
from cuetools.models import AlbumData
from cuetools.parser.parser import load_f_iter


def str_iter(s: str) -> Iterator[str]:
    for line in s.splitlines():
        yield line


def loads(cue: str) -> AlbumData:
    """loading an object from a string, similar to the function json.loads()"""
    return load_f_iter(str_iter(cue))


def load(fp: IO[str]) -> AlbumData:
    """loading an object from a file pointer, similar to the function json.load()"""
    return load_f_iter(fp)
