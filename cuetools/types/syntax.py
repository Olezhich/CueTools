from enum import Enum
from cuetools.types.lex import Token, lex


class States(Enum):
    START = 'start'
    EXPECT_SPACE = 'expect_space'
    EXPECT_WORD = 'expect_word'


def syntax(title: str) -> bool:
    state = States.START
    for token in lex(title=title):
        if state == States.START:
            if any(token == i for i in [Token.CAPITAL_WORD, Token.NUM]):
                state = States.EXPECT_SPACE
            else:
                return False
        elif state == States.EXPECT_SPACE:
            if token == Token.SPACE:
                state = States.EXPECT_WORD
            else:
                return False
        elif state == States.EXPECT_WORD:
            if any(token == i for i in [Token.CAPITAL_WORD, Token.NUM]):
                state = States.EXPECT_SPACE
            else:
                return False
    return True
