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
            cuetools.loads(cue_sample_one_file_one_track_default,)
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
            cuetools.loads(cue_sample_one_file_one_track_strict)
            == obj_sample_one_file_one_track_strict
        )

    def test_one_file_many_tracks(
        self,
        cue_sample_one_file_many_tracks_strict: str,
        obj_sample_one_file_many_tracks_strict: AlbumData,
    ):
        assert (
            cuetools.loads(cue_sample_one_file_many_tracks_strict)
            == obj_sample_one_file_many_tracks_strict
        )


def test_line_parsing():
    cue_sheet = """PERFORMER TITLE"""

    with pytest.raises(cuetools.CueParseError) as e:
        cuetools.loads(cue_sheet)

        assert e.value.got == 'TITLE'

    logger.debug(e.value)

    cue_sheet = """TITLE "The Title Of Album"
                    PERFORMER The Performer"""

    cue = cuetools.loads(cue_sheet)
    logger.debug(cue)

    assert cue == AlbumData(title='The Title Of Album', performer='The Performer')

    cue_sheet = """FILE "The Title Of Album:::"!%^&" WAVE"""
    with pytest.raises(CueParseError) as e:
        cue = cuetools.loads(cue_sheet)
    logger.debug(e.value)

    cue_sheet = """REM"""
    with pytest.raises(cuetools.CueParseError) as e:
        cue = cuetools.loads(cue_sheet)
    logger.debug(e.value)

    cue_sheet = """REM GENRES Blues"""
    with pytest.raises(cuetools.CueParseError) as e:
        cuetools.loads(cue_sheet)
    logger.debug(e.value)

    cue_sheet = """REM DATE wrong1969date"""
    with pytest.raises(cuetools.CueValidationError) as e:
        cuetools.loads(cue_sheet)
    logger.debug(e.value)

    cue_sheet = """REM GENRE Blues
                    REM DATE 1969"""

    cue = cuetools.loads(cue_sheet)
    logger.debug(cue)

    assert cue == AlbumData(rem=RemData(genre='Blues', date=1969))

    cue_sheet = """REM REPLAYGAIN_ALBUM_GAIN 12.5"""
    with pytest.raises(cuetools.CueValidationError) as e:
        cue = cuetools.loads(cue_sheet)
    logger.debug(e.value)

    cue_sheet = """REM REPLAYGAIN_ALBUM_GAIN 5.44 dB
                    REM REPLAYGAIN_ALBUM_PEAK 0.987654"""

    cue = cuetools.loads(cue_sheet)
    logger.debug(cue)


# def test_load_one_track_one_file(
#     cue_sample_one_file_one_track_no_quotes: str,
#     cue_sample_one_file_one_track_rem_quotes: str,
#     cue_sample_one_file_one_track_meta_quotes: str,
#     cue_sample_one_file_one_track_rem_meta_quotes: str,
#     obj_sample_one_file_one_track: cuetools.AlbumData,
# ):
#     """basic loading case: many tracks for one cue sheet via many flac files"""
#     target = obj_sample_one_file_one_track
#     res = cuetools.loads(cue_sample_one_file_one_track_no_quotes)
#     print(repr(res))
#     assert res == target, 'loading: one_file_one_track_no_quotes'

#     res = cuetools.loads(cue_sample_one_file_one_track_rem_quotes)
#     print(repr(res))
#     assert res == target, 'loading: one_file_one_track_rem_quotes'

#     res = cuetools.loads(cue_sample_one_file_one_track_meta_quotes)
#     print(repr(res))
#     assert res == target, 'loading: one_file_one_track_meta_quotes'

#     res = cuetools.loads(cue_sample_one_file_one_track_rem_meta_quotes)
#     print(repr(res))
#     assert res == target, 'loading: one_file_one_track_rem_meta_quotes'


# def test_load_many_tracks_one_file(
#     cue_sample_one_file_many_tracks: str,
#     obj_sample_one_file_many_tracks: cuetools.AlbumData,
# ):
#     """basic loading case: many tracks for one cue sheet via one flac file"""
#     target = obj_sample_one_file_many_tracks
#     res = cuetools.loads(cue_sample_one_file_many_tracks)
#     print(repr(res))
#     assert res == target, 'loading: cue_sample_one_file_many_tracks'


# def test_dump_one_track_one_file(
#     cue_sample_one_file_one_track_no_quotes: str,
#     cue_sample_one_file_one_track_rem_meta_quotes: str,
#     obj_sample_one_file_one_track: cuetools.AlbumData,
# ):
#     """basic dumping case: many tracks for one cue sheet via many flac files"""
#     target = cue_sample_one_file_one_track_no_quotes
#     res = cuetools.dumps(obj_sample_one_file_one_track)
#     assert res == target, 'dumping: one_file_one_track_no_quotes'
#     target = cue_sample_one_file_one_track_rem_meta_quotes
#     res = cuetools.dumps(obj_sample_one_file_one_track, quotes=True)
#     assert res == target, 'dumping: one_file_one_track_rem_meta_quotes'


# # def test_load_rem(obj_sample_rem, cue_sample_rem):
# #     target = obj_sample_rem
# #     res = cuetools.loads(cue_sample_rem)
# #     assert res == target, 'loading: rem'
