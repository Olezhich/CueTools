from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field

from cuetools.types import FrameTime, ReplayGainGain, ReplayGainPeak
from cuetools.cls import FrameTimeCls
from cuetools.types.title_case import TitleCase


class TrackData(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, validate_assignment=True)
    file: Path | None = Field(
        default=None,
        description='Path to the audio file with this track (to flac, ape or etc.) relative to the cue sheet file',
    )
    track: int | None = Field(
        default=None,
        description="Track number, corresponds to the line like *'TRACK 01 AUDIO'*",
    )
    title: str | None = Field(default=None, description='Track title')
    performer: str | None = Field(default=None, description='Track performer')
    index00: FrameTime | None = Field(
        default=None,
        description="The index 00 (the end of the prev track), corresponds to the line like *'INDEX 00 00:00:00'*",
    )
    index01: FrameTime = Field(
        default=FrameTimeCls(0),
        description="The index 01 (the beginning of the current track), corresponds to the line like *'INDEX 01 00:00:00'*",
    )

    def set_performer(self, performer: TitleCase) -> None:
        self.performer = performer
    
    def set_title(self, title: TitleCase) -> None:
        self.title = title



class RemData(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    genre: str | None = Field(default=None, description='Album genre')
    date: int | None = Field(default=None, description='Album release date')
    replaygain_album_gain: ReplayGainGain | None = Field(
        default=None, description='Album replay gain, value format [-]a.bb dB'
    )
    replaygain_album_peak: ReplayGainPeak | None = Field(
        default=None, description='Album peak, value format c.dddddd'
    )

    def set_genre(self, genre: TitleCase) -> None:
        self.genre = genre


class AlbumData(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    performer: str | None = Field(default=None, description='Album performer')
    title: str | None = Field(default=None, description='Album title')
    rem: RemData = Field(
        default_factory=RemData, description='Album additional rem meta'
    )
    tracks: list[TrackData] = Field(
        default_factory=list[TrackData], description='Track list of this album'
    )
    def add_track(self, track : TrackData) -> None:
        self.tracks.append(track)

    def set_performer(self, performer: TitleCase) -> None:
        self.performer = performer
    
    def set_title(self, title: TitleCase) -> None:
        self.title = title

    def __repr__(self) -> str:
        tracks = str(',\n' + ' '*8).join(repr(track) for track in self.tracks)
        return f'AlbumData(\n'\
        f'    performer={self.performer!r},\n'\
        f'    title={self.title!r},\n'\
        f'    rem={repr(self.rem)},\n'\
        f'    tracks=[\n        {tracks}\n    ]\n)'
