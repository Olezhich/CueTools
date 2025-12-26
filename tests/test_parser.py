import pytest
import cuetools

import logging

from cuetools.models import AlbumData, RemData
from cuetools.parser.errors import CueParseError

logger = logging.getLogger(__name__)


class TestLoadDefault:
    def test_one_file_one_track(
        self,
        cue_sample_one_file_one_track_default: str,
        obj_sample_one_file_one_track_default: AlbumData,
    ):
        assert (
            cuetools.loads(
                cue_sample_one_file_one_track_default,
            )
            == obj_sample_one_file_one_track_default
        )

    def test_one_file_many_tracks(
        self,
        cue_sample_one_file_many_tracks_default: str,
        obj_sample_one_file_many_tracks_default: AlbumData,
    ):
        assert (
            cuetools.loads(cue_sample_one_file_many_tracks_default)
            == obj_sample_one_file_many_tracks_default
        )


class TestLoadStrict:
    def test_one_file_one_track(
        self,
        cue_sample_one_file_one_track_strict: str,
        obj_sample_one_file_one_track_strict: AlbumData,
    ):
        assert (
            cuetools.loads(cue_sample_one_file_one_track_strict, strict_title_case=True)
            == obj_sample_one_file_one_track_strict
        )

    def test_one_file_many_tracks(
        self,
        cue_sample_one_file_many_tracks_strict: str,
        obj_sample_one_file_many_tracks_strict: AlbumData,
    ):
        assert (
            cuetools.loads(
                cue_sample_one_file_many_tracks_strict, strict_title_case=True
            )
            == obj_sample_one_file_many_tracks_strict
        )

    def test_real_cue(self, cue_sample_real: str):
        res = cuetools.loads(cue_sample_real, strict_title_case=True)
        assert res.performer == 'Scorpions', (
            'Thats correct if it can parse the entire file without throwing an errors'
        )


def test_line_parsing():
    cue_sheet = """PERFORMER TITLE"""

    with pytest.raises(cuetools.CueParseError) as e:
        cuetools.loads(cue_sheet)

        assert e.value.got == 'TITLE'

    logger.debug(str(e.value))

    cue_sheet = """TITLE "The Title Of Album"
                    PERFORMER The Performer"""

    cue = cuetools.loads(cue_sheet)
    logger.debug(cue)

    assert cue == AlbumData(title='The Title Of Album', performer='The Performer')

    cue_sheet = """FILE "The Title Of Album:::"!%^&" WAVE"""
    with pytest.raises(CueParseError) as e:
        cue = cuetools.loads(cue_sheet)
    logger.debug(str(e.value))

    cue_sheet = """REM"""
    with pytest.raises(cuetools.CueParseError) as e:
        cue = cuetools.loads(cue_sheet)
    logger.debug(str(e.value))

    cue_sheet = """REM GENRES Blues"""
    with pytest.raises(cuetools.CueParseError) as e:
        cuetools.loads(cue_sheet)
    logger.debug(str(e.value))

    cue_sheet = """REM DATE wrong1969date"""
    with pytest.raises(cuetools.CueValidationError) as e:
        cuetools.loads(cue_sheet)
    logger.debug(str(e.value))

    cue_sheet = """REM GENRE Blues
                    REM DATE 1969"""

    cue = cuetools.loads(cue_sheet)
    logger.debug(cue)

    assert cue == AlbumData(rem=RemData(genre='Blues', date=1969))

    cue_sheet = """REM REPLAYGAIN_ALBUM_GAIN 12.5"""
    with pytest.raises(cuetools.CueValidationError) as e:
        cue = cuetools.loads(cue_sheet)
    logger.debug(str(e.value))

    cue_sheet = """REM REPLAYGAIN_ALBUM_GAIN 5.44 dB
                    REM REPLAYGAIN_ALBUM_PEAK 0.987654"""

    cue = cuetools.loads(cue_sheet)
    logger.debug(cue)

    cue_sheet = """FILE "track.flac" WAVE
                    TRACK 01 AUDIO
                    INDEX 00 00:00:50
                    INDEX 01 00:00:65"""
    cue = cuetools.loads(cue_sheet)
    logger.debug(cue)

    cue_sheet = """FILE "track.flac" WAVE
                    INDEX 00 00:00:50
                    INDEX 01 00:00:65"""
    with pytest.raises(cuetools.CueParseError) as e:
        cuetools.loads(cue_sheet)
    logger.debug(str(e.value))
