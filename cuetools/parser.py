from collections.abc import Iterator

from pathlib import Path
from typing import IO, Generator

from cuetools import AlbumData, TrackData


import shlex

from cuetools.types.title_case import TitleCase


def extract_word(line: str, n: int) -> str | None:
    try:
        tokens = shlex.split(line)
        print(tokens)
        return tokens[n]
    except (ValueError, IndexError):
        return None


def process_line(line: str, case: str, many: bool = False) -> list[str]:
    line = line[len(case) :]
    tokens = line.split(',') if many else [line]
    return [i.strip().strip('"\'') for i in tokens]


def str_iter(s: str) -> Iterator[str]:
    for line in s.splitlines():
        yield line


def load_f_iter(cue: Iterator[str], strict_title_case: bool = False) -> AlbumData:
    """loading an object from an iterator"""
    album = AlbumData()
    current_track = None
    current_file = None

    for line in cue:
        line = line.strip()

        if line.startswith('PERFORMER') and not current_track:
            performer = process_line(line, 'PERFORMER')[0]
            if strict_title_case:
                album.set_performer(TitleCase(performer))
            else:
                album.performer = performer
        elif line.startswith('TITLE') and not current_track:
            title = process_line(line, 'TITLE')[0]
            if strict_title_case:
                album.set_title(TitleCase(title))
            else:
                album.title = title
        elif line.startswith('FILE'):
            path = process_line(line, 'FILE', many=True)[0]
            last_idx = path.rfind(' ')
            if '.' in path[:last_idx]:
                path = path[:last_idx]
            current_file = path.strip('\'"')

        elif line.startswith('REM GENRE'):
            genre = process_line(line, 'REM GENRE')[0]
            if strict_title_case:
                album.rem.set_genre(TitleCase(genre))
            else:
                album.rem.genre = genre
        elif line.startswith('REM DATE'):
            album.rem.date = int(process_line(line, 'REM DATE')[0])
        elif line.startswith('REM REPLAYGAIN_ALBUM_GAIN'):
            album.rem.replaygain_album_gain = process_line(
                line, 'REM REPLAYGAIN_ALBUM_GAIN'
            )[0]
        elif line.startswith('REM REPLAYGAIN_ALBUM_PEAK'):
            album.rem.replaygain_album_peak = process_line(
                line, 'REM REPLAYGAIN_ALBUM_PEAK'
            )[0]

        elif line.startswith('TRACK'):
            if current_track:
                album.add_track(current_track)
            track = process_line(line, 'TRACK', many=True)[0].split()[0]
            current_track = TrackData(
                track=int(track), file=Path(current_file) if current_file else None
            )

        elif line.startswith('TITLE') and current_track:
            title = process_line(line, 'TITLE')[0]
            if strict_title_case:
                current_track.set_title(TitleCase(title))
            else:
                current_track.title = title
        elif line.startswith('PERFORMER') and current_track:
            performer = process_line(line, 'PERFORMER')[0]
            if strict_title_case:
                current_track.set_performer(TitleCase(performer))
            else:
                current_track.performer = performer
        elif line.startswith('INDEX 00') and current_track:
            idx = process_line(line, 'INDEX 00')[0]
            current_track.index00 = idx
        elif line.startswith('INDEX 01') and current_track:
            idx = process_line(line, 'INDEX 01')[0]
            current_track.index01 = idx

    if current_track:
        album.add_track(current_track)

    return album


def dumps_line_quotes(arg: str, quotes: bool) -> str:
    q = '"' if quotes else ''
    return f'{q}{arg if arg else ""}{q}'


def dump_gen(
    cue: AlbumData, quotes: bool = False, tab: int = 2, rem_dump_all: bool = False
) -> Generator[str, None, None]:
    for field in cue.rem.model_dump().keys():
        if (attr := getattr(cue.rem, field)) or rem_dump_all:
            yield f'REM {field.upper()} {dumps_line_quotes(attr, quotes)}'

    if cue.performer:
        yield f'PERFORMER {dumps_line_quotes(cue.performer, quotes)}'
    if cue.title:
        yield f'TITLE {dumps_line_quotes(cue.title, quotes)}'

    current_file = None
    for track in cue.tracks:
        if track.file != current_file:
            current_file = track.file
            yield f'FILE "{str(current_file)}" WAVE'

        yield f'{" " * tab}TRACK {(str(track.track) if track.track > 9 else "0" + str(track.track)) if track.track else "0" + "1"} AUDIO'
        if track.title:
            yield f'{" " * tab * 2}TITLE "{track.title}"'
        if track.performer:
            yield f'{" " * tab * 2}PERFORMER "{track.performer}"'
        if track.index00:
            yield f'{" " * tab * 2}INDEX 00 {track.index00.string}'
        if track.index01:
            yield f'{" " * tab * 2}INDEX 01 {track.index01.string}'


def loads(cue: str) -> AlbumData:
    """loading an object from a string, similar to the function json.loads()"""
    return load_f_iter(str_iter(cue))


def load(fp: IO[str]) -> AlbumData:
    """loading an object from a file pointer, similar to the function json.load()"""
    return load_f_iter(fp)


def dumps(
    cue: AlbumData, quotes: bool = False, tab: int = 2, rem_dump_all: bool = False
) -> str:
    """dumping an object to a string, similar to the json.dumps()"""
    album = [line for line in dump_gen(cue, quotes, tab, rem_dump_all)]
    return '\n'.join(album)


def dump(
    cue: AlbumData,
    fp: IO[str],
    quotes: bool = False,
    tab: int = 2,
    rem_dump_all: bool = False,
) -> None:
    """dumping an object to a file pointer, similar to the json.dump()"""
    for line in dump_gen(cue, quotes, tab, rem_dump_all):
        fp.write(line)
        fp.write('\n')
