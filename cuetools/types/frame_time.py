from __future__ import annotations

FRAMES_IN_SEC = 75
FRAMES_IN_MIN = 4500


class FrameTimeCls:
    def __init__(self, frames: int) -> None:
        if frames < 0:
            raise ValueError('Expected frames >= 0')
        self.frames: int = frames

    @classmethod
    def frames_f_string(cls, frames: str) -> FrameTimeCls:
        parts = frames.split(':')
        if len(parts) != 3:
            raise ValueError(f'Expected MM:SS:FF, got {frames!r}')

        mm, ss, ff = map(int, parts)
        if not 0 <= ff < FRAMES_IN_SEC:
            raise ValueError('Expected 0 <= FF < 75 in MM:SS:FF')

        if not 0 <= ss < 60:
            raise ValueError('Expected 0 <= SS < 60 in MM:SS:FF')

        return cls(frames=FRAMES_IN_MIN * mm + FRAMES_IN_SEC * ss + ff)

    @property
    def string(self) -> str:
        mm = self.frames // FRAMES_IN_MIN
        total = self.frames % FRAMES_IN_MIN
        ss = total // FRAMES_IN_SEC
        return f'{mm:02d}:{ss:02d}:{total % FRAMES_IN_SEC:02d}'

    @property
    def seconds(self) -> float:
        return float(self.frames) / FRAMES_IN_SEC

    def __str__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return f'FrameTime(frames={self.frames})'

    def __hash__(self) -> int:
        return hash(self.frames)

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, FrameTimeCls):
            return False
        return self.frames == value.frames
