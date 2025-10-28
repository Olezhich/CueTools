from pathlib import Path
from pydantic import BaseModel, ConfigDict, Field

from cuetools.types import FrameTime, ReplayGainGain, ReplayGainPeak, TitleCaseStr
from cuetools.cls import FrameTimeCls


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
    title: TitleCaseStr | None = Field(default=None, description='Track title')
    performer: TitleCaseStr | None = Field(default=None, description='Track performer')
    index00: FrameTime = Field(
        default=FrameTimeCls(0),
        description="The index 00 (the end of the prev track), corresponds to the line like *'INDEX 00 00:00:00'*",
    )
    index01: FrameTime = Field(
        default=FrameTimeCls(0),
        description="The index 01 (the beginning of the current track), corresponds to the line like *'INDEX 01 00:00:00'*",
    )


class RemData(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    genre: TitleCaseStr | None = Field(default=None, description='Album genre')
    date: int | None = Field(default=None, description='Album release date')
    replaygain_album_gain: ReplayGainGain | None = Field(
        default=None, description='Album replay gain, value format [-]a.bb dB'
    )
    replaygain_album_peak: ReplayGainPeak | None = Field(
        default=None, description='Album peak, value format c.dddddd'
    )


class AlbumData(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    performer: TitleCaseStr | None = Field(default=None, description='Album performer')
    title: TitleCaseStr | None = Field(default=None, description='Album title')
    rem: RemData = Field(
        default_factory=RemData, description='Album additional rem meta'
    )
    tracks: list[TrackData] = Field(
        default_factory=list[TrackData], description='Track list of this album'
    )
    def add_track(self, track : TrackData) -> None:
        self.tracks.append(track)
