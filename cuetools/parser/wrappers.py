from typing import IO, Iterator
from cuetools.models import AlbumData
from cuetools.parser.parser import load_f_iter


def str_iter(s: str) -> Iterator[str]:
    for line in s.splitlines():
        yield line


def loads(cue: str, strict_title_case: bool = False) -> AlbumData:
    """Parse a CUE sheet from a string, similar to the function json.loads().

    Args:
        cue: Full CUE sheet as a string.
        strict_title_case: strict_title_case: If True, require title-case in text fields
                           (e.g., 'Track Title' not 'TRACK title'). Raises CueValidationError
                           on violation. Defaults to False.

    Returns:
        Parsed album data.

    Raises:
        CueParseError: If syntax is invalid.
        CueValidationError: If data is invalid.
    """
    return load_f_iter(str_iter(cue), strict_title_case=strict_title_case)


def load(fp: IO[str], strict_title_case: bool = False) -> AlbumData:
    """Parse a CUE sheet from a file pointer, similar to the function json.loads().

    Args:
        cue: Full CUE sheet as a string.
        strict_title_case: strict_title_case: If True, require title-case in text fields
                           (e.g., 'Track Title' not 'TRACK title'). Raises CueValidationError
                           on violation. Defaults to False.

    Returns:
        Parsed album data.

    Raises:
        CueParseError: If syntax is invalid.
        CueValidationError: If data is invalid.
    """
    return load_f_iter(fp, strict_title_case=strict_title_case)
