from pydantic import ValidationError
import pytest
from cuetools import TrackData
from cuetools.models import AlbumData, RemData
from cuetools.types.title_case import TitleCase


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


def test_ReplayGain_peak():
    rem = RemData(replaygain_album_peak='0.987654')  # type: ignore
    assert rem.replaygain_album_peak == 0.987654, (
        'using string to ReplayGain peak cast, >0 case'
    )

    with pytest.raises(ValidationError):
        RemData(replaygain_album_peak='0.0023')  # type: ignore

    with pytest.raises(ValidationError):
        RemData(replaygain_album_peak='0.0001112')  # type: ignore

    with pytest.raises(ValidationError):
        RemData(replaygain_album_peak='-0.001122')  # type: ignore


def test_TitleCase():
    album = AlbumData(title=TitleCase('The Title'))
    assert album.title == 'The Title', 'only 2 capital words'

    with pytest.raises(ValueError):
        album.set_title(TitleCase('the Title'))

    album.set_title(TitleCase("Now You're Talkin'"))
    assert album.title == "Now You're Talkin'", 'capital words and apostrophe'
