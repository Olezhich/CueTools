from curses.ascii import isdigit
from pathlib import Path
from typing import Any

import pytest
from cuetools import AlbumData, TrackData
from cuetools.models import AlbumRemData, TrackRemData

TAB = 2


def track_gen(
    filename: str,
    songname: str,
    gain: float,
    peak: float,
    tracks_count: int = 1,
    tab: int = TAB,
) -> str:
    out = f'''FILE "{filename}" {'WAVE' if filename.endswith('.flac') else ''}\n'''
    filename = filename.split('.')[0]
    if isdigit(filename[-1]) and isdigit(filename[-2]):
        suf = int(filename[-2:])
    else:
        suf = 1
    for _ in range(tracks_count):
        s = str(suf)
        s = '0' + s if len(s) < 2 else s
        out += f'''{' ' * tab}TRACK {s} AUDIO
{' ' * 2 * tab}TITLE "{songname}"
{' ' * 2 * tab}REM REPLAYGAIN_TRACK_GAIN {gain:.2f} dB
{' ' * 2 * tab}REM REPLAYGAIN_TRACK_PEAK {peak:.6f}
{' ' * 2 * tab}INDEX 01 00:00:00\n'''
        suf += 1
    if out.endswith('\n'):
        out = out[:-1]
    return out


def album_meta_gen(quotes: bool = False, **kwargs: str | list[str]) -> list[str]:
    if not quotes:
        return [
            f'{key.upper()} {", ".join(lst) if isinstance(lst, list) else lst}'
            for key, lst in kwargs.items()
        ]
    tags = []
    for key, lst in kwargs.items():
        s = key.upper() + ' '
        if isinstance(lst, list):
            s += ', '.join(f'"{i}"' for i in lst)
        else:
            s += f'"{lst}"'
        tags.append(s)  # type: ignore
    return tags  # type: ignore


def album_rem_gen(quotes: bool = False, **kwargs: str | list[str]) -> list[str]:
    return [f'REM {i}' for i in album_meta_gen(quotes, **kwargs)]


# FIXTURES

# Meta


@pytest.fixture(params=[False, True])
def album_meta_default(request: Any) -> list[str]:
    return album_meta_gen(
        request.param, performer='the performer', title='the title of album'
    )


@pytest.fixture(params=[False, True])
def album_meta_strict(request: Any) -> list[str]:
    return album_meta_gen(
        request.param, performer='The Performer', title='The Title Of Album'
    )


# Rem


@pytest.fixture(params=[False, True])
def album_rem_default(request: Any) -> list[str]:
    return album_rem_gen(request.param, genre='rock', date='1969')


@pytest.fixture(params=[False, True])
def album_rem_strict(request: Any) -> list[str]:
    return album_rem_gen(request.param, genre='Rock', date='1969')


# Tracks


@pytest.fixture()
def album_tracks_default() -> list[str]:
    return [
        track_gen(f'0{i} - Song 0{i}.flac', f'song {i}', 10.0, 0.9) for i in range(1, 8)
    ]


@pytest.fixture()
def album_tracks_strict() -> list[str]:
    return [
        track_gen(f'0{i} - Song 0{i}.flac', f'Song {i}', 10.0, 0.9) for i in range(1, 8)
    ]


# Cues

# one FILE one track case


@pytest.fixture()
def cue_sample_one_file_one_track_default(
    album_meta_default: list[str],
    album_rem_default: list[str],
    album_tracks_default: list[str],
) -> str:
    cuesheet = album_meta_default + album_rem_default + album_tracks_default
    return '\n'.join(cuesheet)


@pytest.fixture()
def cue_sample_one_file_one_track_strict(
    album_meta_strict: list[str],
    album_rem_strict: list[str],
    album_tracks_strict: list[str],
) -> str:
    cuesheet = album_meta_strict + album_rem_strict + album_tracks_strict
    return '\n'.join(cuesheet)


# one FILE many tracks case


@pytest.fixture()
def cue_sample_one_file_many_tracks_default(
    album_meta_default: list[str], album_rem_default: list[str]
) -> str:
    cuesheet = album_meta_default + album_rem_default
    cuesheet += [track_gen('The Title Of Album.flac', 'track title', 10.0, 0.9, 7)]
    return '\n'.join(cuesheet)


@pytest.fixture()
def cue_sample_one_file_many_tracks_strict(
    album_meta_strict: list[str], album_rem_strict: list[str]
) -> str:
    cuesheet = album_meta_strict + album_rem_strict
    cuesheet += [track_gen('The Title Of Album.flac', 'Track Title', 10.0, 0.9, 7)]
    return '\n'.join(cuesheet)


# Objects

# one FILE one track case


@pytest.fixture()
def obj_sample_one_file_one_track_default() -> AlbumData:
    album = AlbumData(
        performer='the performer',
        title='the title of album',
        rem=AlbumRemData(genre='rock', date=1969),
    )
    for i in range(1, 8):
        album.add_track(
            TrackData(
                track=i,
                title=f'song {i}',
                file=Path(f'0{i} - Song 0{i}.flac'),
                rem=TrackRemData(replaygain_gain=10.0, replaygain_peak=0.9),
            )
        )
    return album


@pytest.fixture()
def obj_sample_one_file_one_track_strict() -> AlbumData:
    album = AlbumData(
        performer='The Performer',
        title='The Title Of Album',
        rem=AlbumRemData(genre='Rock', date=1969),
    )
    for i in range(1, 8):
        album.add_track(
            TrackData(
                track=i,
                title=f'Song {i}',
                file=Path(f'0{i} - Song 0{i}.flac'),
                rem=TrackRemData(replaygain_gain=10.0, replaygain_peak=0.9),
            )
        )
    return album


# one FILE many tracks case


@pytest.fixture()
def obj_sample_one_file_many_tracks_default() -> AlbumData:
    album = AlbumData(
        performer='the performer',
        title='the title of album',
        rem=AlbumRemData(genre='rock', date=1969),
    )
    for i in range(1, 8):
        album.add_track(
            TrackData(
                track=i,
                title='track title',
                file=Path('The Title Of Album.flac'),
                rem=TrackRemData(replaygain_gain=10.0, replaygain_peak=0.9),
            )
        )
    return album


@pytest.fixture()
def obj_sample_one_file_many_tracks_strict() -> AlbumData:
    album = AlbumData(
        performer='The Performer',
        title='The Title Of Album',
        rem=AlbumRemData(genre='Rock', date=1969),
    )
    for i in range(1, 8):
        album.add_track(
            TrackData(
                track=i,
                title='Track Title',
                file=Path('The Title Of Album.flac'),
                rem=TrackRemData(replaygain_gain=10.0, replaygain_peak=0.9),
            )
        )
    return album


@pytest.fixture()
def cue_sample_one_file_many_tracks() -> str:
    cuesheet = album_rem_default() + album_meta_default()
    cuesheet += [track_gen('The Title Of Album.flac', 'song_name', 10.0, 0.9, 7)]
    return '\n'.join(cuesheet)


@pytest.fixture()
def obj_sample_one_file_many_tracks() -> AlbumData:
    album = AlbumData(
        performer='The Performer',
        title='The Title Of Album',
        rem=AlbumRemData(genre='Rock', date=1969),
    )
    for i in range(1, 8):
        album.add_track(
            TrackData(
                track=i,
                title='song_name',
                file=Path('The Title Of Album.flac'),
                rem=TrackRemData(replaygain_gain=10.0, replaygain_peak=0.9),
            )
        )
    return album


@pytest.fixture()
def cue_sample_real() -> str:
    return """REM GENRE Hard Rock
REM DATE 1972
REM DISCID 12345678
REM COMMENT ExactAudioCopy v1.0b3
PERFORMER "Scorpions"
TITLE "Lonesome Crow"
REM REPLAYGAIN_ALBUM_GAIN -7.99 dB
REM REPLAYGAIN_ALBUM_PEAK 1.054599
FILE "Scorpions - Lonesome Crow.flac" WAVE
  TRACK 01 AUDIO
    TITLE "I'm Going Mad"
    REM REPLAYGAIN_TRACK_GAIN -7.97 dB
    REM REPLAYGAIN_TRACK_PEAK 1.033902
    INDEX 01 00:00:00
  TRACK 02 AUDIO
    TITLE "It All Depends"
    REM REPLAYGAIN_TRACK_GAIN -8.17 dB
    REM REPLAYGAIN_TRACK_PEAK 1.054599
    INDEX 01 04:53:27
  TRACK 03 AUDIO
    TITLE "Leave Me"
    REM REPLAYGAIN_TRACK_GAIN -8.56 dB
    REM REPLAYGAIN_TRACK_PEAK 1.053317
    INDEX 00 08:17:15
    INDEX 01 08:18:42
  TRACK 04 AUDIO
    TITLE "In Search Of The Peace Of Mind"
    REM REPLAYGAIN_TRACK_GAIN -6.73 dB
    REM REPLAYGAIN_TRACK_PEAK 1.035224
    INDEX 00 13:21:00
    INDEX 01 13:22:52
  TRACK 05 AUDIO
    TITLE "Inheritance"
    REM REPLAYGAIN_TRACK_GAIN -8.17 dB
    REM REPLAYGAIN_TRACK_PEAK 1.038148
    INDEX 00 18:16:10
    INDEX 01 18:17:62
  TRACK 06 AUDIO
    TITLE "Action"
    REM REPLAYGAIN_TRACK_GAIN -8.43 dB
    REM REPLAYGAIN_TRACK_PEAK 1.031126
    INDEX 00 22:55:50
    INDEX 01 22:58:17
  TRACK 07 AUDIO
    TITLE "Lonesome Crow"
    REM REPLAYGAIN_TRACK_GAIN -7.85 dB
    REM REPLAYGAIN_TRACK_PEAK 1.042687
    INDEX 00 26:51:00
    INDEX 01 26:52:37
"""
