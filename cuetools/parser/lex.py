from enum import Enum
import re
from typing import Generator, NamedTuple


class Token(Enum):
    WHITE_SPACE = r'(\s+)'
    PERFORMER = r'(PERFORMER)\b'
    TITLE = r'(TITLE)\b'

    FILE = r'(FILE)\b'
    WAVE = r'(WAVE)\b'

    REM = r'(REM)\b'
    GENRE = r'(GENRE)\b'
    DATE = r'(DATE)\b'

    REPLAYGAIN_ALBUM_GAIN = r'(REPLAYGAIN_ALBUM_GAIN)\b'
    REPLAYGAIN_ALBUM_PEAK = r'(REPLAYGAIN_ALBUM_PEAK)\b'
    REPLAYGAIN_TRACK_GAIN = r'(REPLAYGAIN_TRACK_GAIN)\b'
    REPLAYGAIN_TRACK_PEAK = r'(REPLAYGAIN_TRACK_PEAK)\b'

    DISCID = r'(DISCID)\b'
    COMMENT = r'(COMMENT)\b'

    TRACK = r'TRACK (\d\d+)\b'
    AUDIO = r'(AUDIO)\b'
    INDEX = r'INDEX (\d\d)\b'

    ARG_QUOTES = r'"(.*)"'
    ARG = r'(.*)'

    def __init__(self, pattern: str) -> None:
        self.regex = re.compile(pattern)


class TokenMatch(NamedTuple):
    type: Token
    lexeme: str
    pos: int


def lex(line: str) -> Generator[TokenMatch, None, None]:
    pos = 0
    length = len(line)
    while pos < length:
        matched = False
        for token in Token:
            match = token.regex.match(line, pos)
            if match:
                matched = True
                if token is not Token.WHITE_SPACE:
                    yield TokenMatch(token, match.group(1), pos)
                pos = match.end()
                break
        if not matched:
            raise ValueError('Impossible to obtain any token')
