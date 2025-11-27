from pydantic import ValidationError


class CueBaseError(ValueError):
    def __init__(self, line: int, line_content: str, pos: int, got: str) -> None:
        self.line = line
        self.line_content = line_content
        self.pos = pos
        self.got = got
        super().__init__()

    def _format_msg(self) -> str:
        return '\n'.join(
            [
                f'\nLine {self.line}: pos {self.pos}',
                '  ' + self.line_content,
                '  ' + ' ' * (self.pos) + '^' * len(self.got),
            ]
        )

    def __str__(self) -> str:
        return self._format_msg()


class CueParseError(CueBaseError):
    """Raised when CUE sheet syntax is invalid."""

    def __init__(
        self, line: int, line_content: str, expected: str, got: str, pos: int
    ) -> None:
        super().__init__(line, line_content, pos, got)
        self.expected = expected

    def _format_msg(self):
        header = f'Expected: {self.expected} Got: {self.got}'
        return header + super()._format_msg()


class CueValidationError(CueBaseError):
    """Raised when semantic rules are violated."""

    def __init__(
        self,
        line: int,
        line_content: str,
        pos: int,
        got: str,
        validation_error: ValidationError | ValueError,
    ) -> None:
        super().__init__(line, line_content, pos, got)
        self.validation_error = validation_error

    def _format_msg(self) -> str:
        header = (
            str(self.validation_error.json(indent=4))
            if isinstance(self.validation_error, ValidationError)
            else self.validation_error.args[0]
        )
        return header + super()._format_msg()
