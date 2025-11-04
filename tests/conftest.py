from curses.ascii import isdigit
from pathlib import Path
# from shlex import quote

import pytest
from cuetools import AlbumData, TrackData
from cuetools.models import RemData

TAB = 2


def track_gen(
    filename: str, songname: str, tracks_count: int = 1, tab: int = TAB
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


def album_rem_default(quotes: bool = False) -> list[str]:
    return album_rem_gen(quotes, genre='Rock', date='1969')  # , comment='comment')


def album_meta_default(quotes: bool = False) -> list[str]:
    return album_meta_gen(quotes, performer='The Performer', title='The Title Of Album')


@pytest.fixture()
def cue_sample_one_file_one_track_no_quotes() -> str:
    cuesheet = album_rem_default() + album_meta_default()
    cuesheet += [track_gen(f'0{i} - Song 0{i}.flac', f'Song {i}') for i in range(1, 8)]
    return '\n'.join(cuesheet)


@pytest.fixture()
def cue_sample_one_file_one_track_rem_quotes() -> str:
    cuesheet = album_rem_default(True) + album_meta_default()
    cuesheet += [track_gen(f'0{i} - Song 0{i}.flac', f'Song {i}') for i in range(1, 8)]
    return '\n'.join(cuesheet)


@pytest.fixture()
def cue_sample_one_file_one_track_meta_quotes() -> str:
    cuesheet = album_rem_default() + album_meta_default(True)
    cuesheet += [track_gen(f'0{i} - Song 0{i}.flac', f'Song {i}') for i in range(1, 8)]
    return '\n'.join(cuesheet)


@pytest.fixture()
def cue_sample_one_file_one_track_rem_meta_quotes() -> str:
    cuesheet = album_rem_default(True) + album_meta_default(True)
    cuesheet += [track_gen(f'0{i} - Song 0{i}.flac', f'Song {i}') for i in range(1, 8)]
    return '\n'.join(cuesheet)


@pytest.fixture()
def obj_sample_one_file_one_track() -> AlbumData:
    album = AlbumData(
        performer='The Performer',
        title='The Title Of Album',
        rem=RemData(genre='Rock', date=1969),
    )
    for i in range(1, 8):
        album.add_track(
            TrackData(track=i, title=f'Song {i}', file=Path(f'0{i} - Song 0{i}.flac'))
        )
    return album


@pytest.fixture()
def cue_sample_one_file_many_tracks() -> str:
    cuesheet = album_rem_default() + album_meta_default()
    cuesheet += [track_gen('The Title Of Album.flac', 'song_name', 7)]
    return '\n'.join(cuesheet)


@pytest.fixture()
def obj_sample_one_file_many_tracks() -> AlbumData:
    album = AlbumData(
        performer='The Performer',
        title='The Title Of Album',
        rem=RemData(genre='Rock', date=1969),
    )
    for i in range(1, 8):
        album.add_track(
            TrackData(track=i, title='song_name', file=Path('The Title Of Album.flac'))
        )
    return album


@pytest.fixture()
def cue_sample_rem():
    album = album_rem_gen(
        genre='Hard Rock',
        date='1969',
        replaygain_album_gain='-4.10 db',
        replaygain_album_peak='0.987654',
    )
    return '\n'.join(album)


@pytest.fixture()
def obj_sample_rem() -> AlbumData:
    album = AlbumData(
        rem=RemData(
            genre='Hard Rock',
            date=1969,
            replaygain_album_gain='-4.10 db',  # type: ignore
            replaygain_album_peak='0.987654',  # type: ignore
        )
    )
    return album


if __name__ == '__main__':
    print('___album rem tests___')

    print(album_rem_gen(genre='Rock', date='1969', comment='comment'))
    print(
        album_rem_gen(
            genre=['Hard Rock', 'Progressive Rock', 'Rock'],
            date='1969',
            comment='comment',
        )
    )
    print(album_rem_gen(quotes=True, genre='Rock', date='1969', comment='comment'))
    print(
        album_rem_gen(
            quotes=True,
            genre=['Hard Rock', 'Progressive Rock', 'Rock'],
            date='1969',
            comment='comment',
        )
    )

    print('___album meta tests___')

    print(album_meta_gen(performer='The Performer', title='The Title Of Album'))
    print(
        album_meta_gen(
            quotes=True, performer='The Performer', title='The Title Of Album'
        )
    )

    print('___another tests___')

    print(track_gen('song.flac', 'song', 3))
    print(track_gen('song 05.flac', 'song', 1))
    print([track_gen(f'0{i} - Song 0{i}.flac', f'Song {i}') for i in range(1, 8)])

    print('___cue_gen_test___')

    cuesheet = album_rem_default() + album_meta_default()
    cuesheet += [track_gen(f'0{i} - Song 0{i}.flac', f'Song {i}') for i in range(1, 8)]
    # for i in cuesheet:
    #     print(i.endswith('\n'), i)

    # cuesheet = [i[-1:] if i.endswith('\n') else i for i in cuesheet]
    print('\n'.join(cuesheet))
