class CueParseError(ValueError):
    def __init__(
        self, line: int, line_content: str, expected: str, got: str, pos: int
    ) -> None:
        self.line = line
        self.line_content = line_content
        self.expected = expected
        self.got = got
        self.pos = pos
        super().__init__(self._format_msg())

    def _format_msg(self):
        return '\n'.join(
            [
                f'Line {self.line}: Expected: {self.expected} Got: {self.got}',
                '  ' + self.line_content,
                '  ' + ' ' * (self.pos) + '^' * len(self.got),
            ]
        )
