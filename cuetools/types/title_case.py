from __future__ import annotations

from cuetools.types.syntax import syntax


class TitleCase(str):
    def __new__(cls, title: str) -> TitleCase:
        if syntax(title=title):
            return super().__new__(cls, title)
        raise ValueError('Expected Title Case string')
