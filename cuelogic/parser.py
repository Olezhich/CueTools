import os.path

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

def load(cue : str) -> AlbumData:
    album = AlbumData()
    dir = '' #os.path.dirname(path)
    current_track = None
    current_file = None

    for line in cue.splitlines():
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
            file_path = dir + path.strip('\'\"')
            current_file = file_path
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
            current_track.add_index((idx[0],idx[1]))
    if current_track:
        album.add_track(current_track)

    #with open(path, 'r') as f:


    return album

if __name__ == '__main__':
    print('___process_line_tests___')
    print(process_line('REM DATE 1969', 'REM DATE'))
    print(process_line('REM DATE "1969"', 'REM DATE'))
    print(process_line('REM DATE 1969, 1975', 'REM DATE', many=True))
    print(process_line('REM DATE "1969", "1975"', 'REM DATE', many=True))
    print(process_line('INDEX 01 00:00:00', 'INDEX', many=True))
    print(process_line('FILE "06 - Song 6.flac" WAVE', 'FILE'))
    print(process_line('FILE 06 - Song 6.flac WAVE', 'FILE'))

