from enum import StrEnum
from cuetools.types.lex import Token, lex

class States(StrEnum):
    START = 'start'
    EXPECT_SPACE = 'expect_space'
    EXPECT_WORD = 'expect_word'


def syntax(title: str) -> bool:
    state = States.START
    for token in lex(title=title):
        if state == States.START:
            if token == Token.CAPITAL_WORD:
                state = States.EXPECT_SPACE
            else:
                return False
        elif state == States.EXPECT_SPACE:
            if token == Token.SPACE:
                state = States.EXPECT_WORD
            else:
                return False
        elif state == States.EXPECT_WORD:
            if token == Token.CAPITAL_WORD:
                state = States.EXPECT_SPACE
            else:
                return False
    return True