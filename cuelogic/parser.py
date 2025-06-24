import os.path
from collections.abc import Iterator

from cuelogic import AlbumData, TrackData

import shlex

def extract_word(line : str, n : int) -> str | None:
    try:
        tokens = shlex.split(line)
        print(tokens)
        return tokens[n]
    except (ValueError, IndexError):
        return None

def process_line(line : str, case : str, many : bool=False) -> list[str]:
    line = line[len(case):]
    tokens = line.split(',') if many else [line]
    return [i.strip().strip('\"\'') for i in tokens]

def str_iter(s : str) -> Iterator[str]:
    for line in s.splitlines():
        yield line


def load_f_iter(cue : Iterator[str]) -> AlbumData:
    """loading an object from an iterator"""
    album = AlbumData()
    current_track = None
    current_file = None

    for line in cue:
        line = line.strip()

        if line.startswith("PERFORMER") and not current_track:
            album.set_performer(process_line(line, "PERFORMER")[0])
        elif line.startswith("TITLE") and not current_track:
            album.set_title(process_line(line, "TITLE")[0])
        elif line.startswith("FILE"):
            path = process_line(line, "FILE", many=True)[0]
            last_idx = path.rfind(' ')
            if '.' in path[:last_idx]:
                path = path[:last_idx]
            current_file = path.strip('\'\"')
        elif line.startswith('REM GENRE'):
            album.set_genre(process_line(line, "REM GENRE")[0])
        elif line.startswith('REM DATE'):
            album.set_date(process_line(line, "REM DATE")[0])

        elif line.startswith("TRACK"):
            if current_track:
                album.add_track(current_track)
            track = process_line(line, "TRACK", many=True)[0].split()[0]
            current_track = TrackData(track=track, link=current_file)

        elif line.startswith("TITLE") and current_track:
            current_track.set_title(process_line(line, "TITLE")[0])
        elif line.startswith("PERFORMER") and current_track:
            current_track.set_performer(process_line(line, "PERFORMER")[0])
        elif line.startswith("INDEX") and current_track:
            idx = process_line(line, "INDEX")[0].split()
            current_track.add_index((idx[0], idx[1]))
    if current_track:
        album.add_track(current_track)

    return album

def loads(cue : str) -> AlbumData:
    """loading an object from a string, similar to the function json.loads()"""
    return load_f_iter(str_iter(cue))


if __name__ == '__main__':
    print('___process_line_tests___')
    print(process_line('REM DATE 1969', 'REM DATE'))
    print(process_line('REM DATE "1969"', 'REM DATE'))
    print(process_line('REM DATE 1969, 1975', 'REM DATE', many=True))
    print(process_line('REM DATE "1969", "1975"', 'REM DATE', many=True))
    print(process_line('INDEX 01 00:00:00', 'INDEX', many=True))
    print(process_line('FILE "06 - Song 6.flac" WAVE', 'FILE'))
    print(process_line('FILE 06 - Song 6.flac WAVE', 'FILE'))

