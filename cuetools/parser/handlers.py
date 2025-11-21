from typing import Callable
from cuetools.parser.errors import CueParseError
from cuetools.parser.lex import Token, TokenMatch
from cuetools.types.title_case import TitleCase


def title_case_handler(
    value: TokenMatch,
    strict: bool,
    dto_setter: Callable[[str], None],
    dto_strict_setter: Callable[[TitleCase], None],
    line_idx: int,
    line: str,
    err_expected_comment: str,
) -> None:
    """Set value in default/strict mode, if needs raise a `CueParseError`"""
    match value.type:
        case Token.ARG_QUOTES | Token.ARG:
            if strict:
                dto_strict_setter(TitleCase(value.lexeme))
            else:
                dto_setter(value.lexeme)
        case _:
            raise CueParseError(
                line_idx,
                line,
                err_expected_comment,
                value.lexeme,
                value.pos,
            )
