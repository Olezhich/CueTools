"""Lightweight CUE sheet toolkit for parsing and generating `.cue` files.

Provides `loads()` and `load()` functions to parse CUE sheets into structured
Pydantic models (`AlbumData`, `TrackData`, etc.), and supports serialization
back to CUE format.

Designed to mirror the `json` module API for familiarity.
"""

from .types import FrameTime
from .models import TrackData
from .models import AlbumData

from .parser import load, loads, CueParseError, CueValidationError

__all__ = [
    'FrameTime',
    'TrackData',
    'AlbumData',
    'CueParseError',
    'CueValidationError',
    'loads',
    'load',
]
