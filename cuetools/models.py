from __future__ import annotations
from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field

from cuetools.types import FrameTime, ReplayGainGain, ReplayGainPeak
from cuetools.types.frame_time import FrameTimeCls
from cuetools.types.title_case import TitleCase


class BaseRemData(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    replaygain_gain: ReplayGainGain | None = Field(
        default=None, description='Album replay gain, value format [-]a.bb dB'
    )
    replaygain_peak: ReplayGainPeak | None = Field(
        default=None, description='Album peak, value format c.dddddd'
    )


class AlbumRemData(BaseRemData):
    genre: str | None = Field(default=None, description='Album genre')
    date: int | None = Field(default=None, description='Album release date')

    def set_genre(self, genre: TitleCase) -> None:
        """Set album genre with a Title Case validation using `TitleCase` class consructor for string"""
        self.genre = genre


class TrackRemData(BaseRemData): ...


class TrackData(BaseModel):
    """Represents a single track within a CUE sheet.

    Includes file reference, track number, metadata
    such as title, performer, index, etc."""

    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)
    file: Path = Field(
        description='Path to the audio file with this track (to flac, ape or etc.) relative to the cue sheet file',
    )
    track: int = Field(
        description="Track number, corresponds to the line like *'TRACK 01 AUDIO'*",
    )
    title: str | None = Field(default=None, description='Track title')
    performer: str | None = Field(default=None, description='Track performer')
    rem: TrackRemData = Field(
        default_factory=TrackRemData, description='Track additional rem meta'
    )
    index00: FrameTime | None = Field(
        default=None,
        description="The index 00 (the end of the prev track), corresponds to the line like *'INDEX 00 00:00:00'*",
    )
    index01: FrameTime = Field(
        default=FrameTimeCls(0),
        description="The index 01 (the beginning of the current track), corresponds to the line like *'INDEX 01 00:00:00'*",
    )

    def validate_index(self) -> None:
        if self.index00 is not None and self.index00.frames > self.index01.frames:
            raise ValueError('Expected INDEX 00 <= INDEX 01')

    def set_performer(self, performer: TitleCase) -> None:
        """Set track performer with a **Title Case** validation using `TitleCase` class consructor for string"""
        self.performer = performer

    def set_title(self, title: TitleCase) -> None:
        """Set track title with a **Title Case** validation using `TitleCase` class consructor for string"""
        self.title = title


class AlbumData(BaseModel):
    """Represents a parsed CUE sheet at the album level.

    Contains global metadata (performer, title, etc.) and a list of tracks.
    """

    model_config = ConfigDict(validate_assignment=True)
    performer: str | None = Field(default=None, description='Album performer')
    title: str | None = Field(default=None, description='Album title')
    rem: AlbumRemData = Field(
        default_factory=AlbumRemData, description='Album additional rem meta'
    )
    tracks: list[TrackData] = Field(
        default_factory=list[TrackData], description='Track list of this album'
    )

    def add_track(self, track: TrackData) -> None:
        track.validate_index()
        self.tracks.append(track)

    def set_performer(self, performer: TitleCase) -> None:
        """Set album performer with a **Title Case** validation using `TitleCase` class consructor for string"""
        self.performer = performer

    def set_title(self, title: TitleCase) -> None:
        """Set album title with a **Title Case** validation using `TitleCase` class consructor for string"""
        self.title = title

    def __repr__(self) -> str:
        tracks = str(',\n' + ' ' * 8).join(repr(track) for track in self.tracks)
        return (
            f'AlbumData(\n'
            f'    performer={self.performer!r},\n'
            f'    title={self.title!r},\n'
            f'    rem={repr(self.rem)},\n'
            f'    tracks=[\n        {tracks}\n    ]\n)'
        )
