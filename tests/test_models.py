from pathlib import Path

from pydantic import ValidationError
import pytest
from cuetools import TrackData
from cuetools.models import RemData


def test_TrackData():
    album = TrackData(
        file=Path('/music/album.flac'),
        title='Album Title',
        performer='The Performer',
        index00='00:00:00',  # type: ignore
        index01=50,  # type: ignore
    )
    print(album)


def test_FrameTime():
    track = TrackData(index00='01:50:05', index01=9000)  # type: ignore
    assert track.index00.frames == 8255, 'using string to FrameTime cast'
    assert track.index01.string == '02:00:00', 'using int to FrameTime cast'

    with pytest.raises(ValidationError):
        TrackData(index00='00:61:76')  # type: ignore

    with pytest.raises(ValidationError):
        TrackData(index00='00')  # type: ignore

    with pytest.raises(ValidationError):
        TrackData(index00=-1234)  # type: ignore


def test_ReplayGain_gain():
    rem = RemData(replaygain_album_gain='17.84 dB')  # type: ignore
    assert rem.replaygain_album_gain == 17.84, (
        'using string to ReplayGain gain cast, >0 case'
    )
    rem = RemData(replaygain_album_gain='-17.84 dB')  # type: ignore
    assert rem.replaygain_album_gain == -17.84, (
        'using string to ReplayGain gain cast, <0 case'
    )

    rem = RemData(replaygain_album_gain=17.84)  # type: ignore
    assert rem.replaygain_album_gain == 17.84, (
        'using float to ReplayGain gain cast, >0 case'
    )

    with pytest.raises(ValidationError):
        RemData(replaygain_album_gain='7.8 dB')  # type: ignore

    with pytest.raises(ValidationError):
        RemData(replaygain_album_gain='0.824654')  # type: ignore
