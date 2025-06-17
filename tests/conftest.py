import pytest
from cuelogic import AlbumData, TrackData
from cuelogic.models import RemData

TAB = 2

def track_gen(filename : str, songname : str, tab: int = TAB) -> str:
    return \
f'''FILE "{filename}" {'WAVE' if filename.endswith('.flac') else ''}
{' '*tab}TRACK {filename[:2]} AUDIO
{' '*2*tab}TITLE "{songname}"
{' '*3*tab}INDEX 01 00:00:00'''


@pytest.fixture()
def cue_sample_one_file_one_track() -> str:
    cuesheet = []
    cuesheet += ['REM GENRE Rock', 'REM DATE 1969', 'REM COMMENT comment', 'PERFORMER "The Performer"', 'TITLE "Album 1"']
    cuesheet += [track_gen(f'0{i} - Song {i}.flac', f'Song {i}') for i in range(7)]
    return '\n'.join(cuesheet)

@pytest.fixture()
def obj_sample_one_file_one_track() -> AlbumData:
    album = AlbumData(performer='The Performer', title='Album 1', rem=RemData(genre='Rock', date='1969'))
    for i in range(7):
        album.add_track(TrackData(track=f'0{i}', title=f'Song {i}', link=f'0{i} - Song {i}.flac'))
    return album


