from collections.abc import Iterator
from dataclasses import fields
from typing import IO, Generator

from cuetools import AlbumData, TrackData


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
        elif line.startswith('REM REPLAYGAIN_ALBUM_GAIN'):
            album.set_gain(process_line(line, "REM REPLAYGAIN_ALBUM_GAIN")[0])
        elif line.startswith('REM REPLAYGAIN_ALBUM_PEAK'):
            album.set_peak(process_line(line, "REM REPLAYGAIN_ALBUM_PEAK")[0])

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

def dumps_line_quotes(arg : str, quotes : bool) -> str:
    q = '"' if  quotes else ''
    return f'{q}{arg if arg else ""}{q}'

def dump_gen(cue : AlbumData, quotes : bool=False, tab : int=2, rem_dump_all : bool=False) -> Generator[str, None, None]:
    for field in fields(cue.rem):
        if (attr := getattr(cue.rem, field.name)) or rem_dump_all:
            yield f'REM {field.name.upper()} {dumps_line_quotes(attr, quotes)}'

    yield f'PERFORMER {dumps_line_quotes(cue.performer, quotes)}'
    yield f'TITLE {dumps_line_quotes(cue.title, quotes)}'

    current_file = None
    for track in cue.tracks:
        if track.link != current_file:
            current_file = track.link
            yield f'FILE "{current_file}" WAVE'

        yield f'{" "*tab}TRACK {track.track if track.track else "0" + "1"} AUDIO'
        if track.title:
            yield f'{" "*tab*2}TITLE "{track.title}"'
        if track.performer:
            yield f'{" "*tab*2}PERFORMER "{track.performer}"'
        if track.index:
            for idx in sorted(track.index.keys()):
                yield f'{" "*tab*2}INDEX {idx} {track.index[idx]}'


def loads(cue : str) -> AlbumData:
    """loading an object from a string, similar to the function json.loads()"""
    return load_f_iter(str_iter(cue))

def load(fp : IO[str]) -> AlbumData:
    """loading an object from a file pointer, similar to the function json.load()"""
    return load_f_iter(fp)

def dumps(cue : AlbumData, quotes : bool=False, tab : int=2, rem_dump_all : bool=False) -> str:
    """dumping an object to a string, similar to the json.dumps()"""
    album = [line for line in dump_gen(cue, quotes, tab, rem_dump_all)]
    return '\n'.join(album)

def dump(cue : AlbumData, fp : IO[str], quotes : bool=False, tab : int=2, rem_dump_all : bool=False) -> None:
    """dumping an object to a file pointer, similar to the json.dump()"""
    for line in dump_gen(cue, quotes, tab, rem_dump_all):
        fp.write(line)
        fp.write('\n')