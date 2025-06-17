import os.path

from models import AlbumData, TrackData

import shlex

def extract_word(line : str, n : int) -> str | None:
    try:
        return shlex.split(line)[n]
    except (ValueError, IndexError):
        return None

def load(path : str) -> AlbumData:
    album = AlbumData()
    dir = os.path.dirname(path)
    current_track = None
    current_file = None

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("PERFORMER") and not current_track:
                album.set_performer(extract_word(line, 1))
            elif line.startswith("TITLE") and not current_track:
                album.set_title(extract_word(line, 1))
            elif line.startswith("FILE"):
                file_path = dir + '/' + extract_word(line, 1)
                current_file = file_path
            elif line.startswith('REM GENRE'):
                album.set_genre(extract_word(line, 2))
            elif line.startswith('REM DATE'):
                album.set_date(extract_word(line, 2))

            elif line.startswith("TRACK"):
                if current_track:
                    album.add_track(current_track)
                current_track = TrackData(track=extract_word(line, 1), link=current_file)

            elif line.startswith("TITLE") and current_track:
                current_track.set_title(extract_word(line, 1))
            elif line.startswith("PERFORMER") and current_track:
                current_track.set_performer(extract_word(line, 1))
            elif line.startswith("INDEX") and current_track:
                current_track.add_index((extract_word(line, 1), extract_word(line, 2)))
        if current_track:
            album.add_track(current_track)

    return album