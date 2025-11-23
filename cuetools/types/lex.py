from enum import Enum
import re
from typing import Generator


class Token(Enum):
    CAPITAL_WORD = r'[A-Z][a-z]*(?:\'[a-z]*)?'
    MINOR_WORD = r'[a-z]+'
    SPACE = r' '
    NUM = r'\d+'

    def __init__(self, pattern: str) -> None:
        self.regex = re.compile(pattern)


def lex(title: str) -> Generator[Token, None, None]:
    pos = 0
    length = len(title)
    while pos < length:
        matched = False
        for token in Token:
            match = token.regex.match(title, pos)
            if match:
                matched = True
                yield token
                pos = match.end()
                break
        if not matched:
            raise ValueError('Impossible to obtain any token')
