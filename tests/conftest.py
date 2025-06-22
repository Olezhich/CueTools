from shlex import quote

import pytest
from cuelogic import AlbumData, TrackData
from cuelogic.models import RemData

TAB = 2

def track_gen(filename : str, songname : str, tab: int =TAB) -> str:
    return \
f'''FILE "{filename}" {'WAVE' if filename.endswith('.flac') else ''}
{' '*tab}TRACK {filename[:2]} AUDIO
{' '*2*tab}TITLE "{songname}"
{' '*3*tab}INDEX 01 00:00:00'''

def album_meta_gen(quotes : bool=False, **kwargs : str | list[str]) -> list[str]:
    if not quotes:
        return [f'{key.upper()} {', '.join(lst) if isinstance(lst, list) else lst}' for key, lst in kwargs.items()]
    return [f'{key.upper()} {', '.join(f'"{i}"' for i in lst) if isinstance(lst, list) else f'"{lst}"'}' for key, lst in kwargs.items()]

def album_rem_gen(quotes : bool=False, **kwargs : str | list[str]) -> list[str]:
    return [f'REM {i}' for i in album_meta_gen(quotes, **kwargs)]

def album_rem_default(quotes : bool=False) -> list[str]:
    return album_rem_gen(quotes, genre='Rock', date='1969', comment='comment')

def album_meta_default(quotes : bool=False) -> list[str]:
    return album_meta_gen(quotes, performer='The Performer', title='The Title Of Album')


@pytest.fixture()
def cue_sample_one_file_one_track_no_quotes() -> str:
    cuesheet = album_rem_default() + album_meta_default()
    cuesheet += [track_gen(f'0{i} - Song {i}.flac', f'Song {i}') for i in range(7)]
    return '\n'.join(cuesheet)

@pytest.fixture()
def cue_sample_one_file_one_track_rem_quotes() -> str:
    cuesheet = album_rem_default(True) + album_meta_default()
    cuesheet += [track_gen(f'0{i} - Song {i}.flac', f'Song {i}') for i in range(7)]
    return '\n'.join(cuesheet)

@pytest.fixture()
def cue_sample_one_file_one_track_meta_quotes() -> str:
    cuesheet = album_rem_default() + album_meta_default(True)
    cuesheet += [track_gen(f'0{i} - Song {i}.flac', f'Song {i}') for i in range(7)]
    return '\n'.join(cuesheet)

@pytest.fixture()
def cue_sample_one_file_one_track_rem_meta_quotes() -> str:
    cuesheet = album_rem_default(True) + album_meta_default(True)
    cuesheet += [track_gen(f'0{i} - Song {i}.flac', f'Song {i}') for i in range(7)]
    return '\n'.join(cuesheet)

@pytest.fixture()
def obj_sample_one_file_one_track() -> AlbumData:
    album = AlbumData(performer='The Performer', title='The Title Of Album', rem=RemData(genre='Rock', date='1969'))
    for i in range(7):
        album.add_track(TrackData(track=f'0{i}', title=f'Song {i}', link=f'0{i} - Song {i}.flac'))
    return album

@pytest.fixture()
def cue_sample_one_file_many_tracks() -> str:
    ...

if __name__ == '__main__':
    print('___album rem tests___')

    print(album_rem_gen(genre='Rock', date='1969', comment='comment'))
    print(album_rem_gen(genre=['Hard Rock', 'Progressive Rock', 'Rock'], date='1969', comment='comment'))
    print(album_rem_gen(quotes=True, genre='Rock', date='1969', comment='comment'))
    print(album_rem_gen(quotes=True, genre=['Hard Rock', 'Progressive Rock', 'Rock'], date='1969', comment='comment'))

    print('___album meta tests___')

    print(album_meta_gen(performer='The Performer', title='The Title Of Album'))
    print(album_meta_gen(quotes=True, performer='The Performer', title='The Title Of Album'))

    print('___another tests___')





