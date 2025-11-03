from typing import Iterator
from cuetools.models import AlbumData
from cuetools.parser.errors import CueParseError
from cuetools.parser.lex import Token, lex
from cuetools.types.title_case import TitleCase


def load_f_iter(cue: Iterator[str], strict_title_case: bool = False) -> AlbumData:
    """loading an object from an iterator"""
    album = AlbumData()
    # current_track = None
    # current_file = None

    current_line = 0

    for line in cue:
        current_line += 1
        tokens = [i for i in lex(line)]

        match tokens[0].type:
            case Token.PERFORMER:
                performer = tokens[1]
                match performer.type:
                    case Token.ARG_QUOTES | Token.ARG:
                        if strict_title_case:
                            album.set_performer(TitleCase(performer.lexeme))
                        else:
                            album.performer = performer.lexeme
                    case _:
                        raise CueParseError(
                            current_line,
                            line,
                            'performer name',
                            performer.lexeme,
                            performer.pos,
                        )
            case _:
                ...

    #     if line.startswith('PERFORMER') and not current_track:
    #         performer = process_line(line, 'PERFORMER')[0]
    #         if strict_title_case:
    #             album.set_performer(TitleCase(performer))
    #         else:
    #             album.performer = performer
    #     elif line.startswith('TITLE') and not current_track:
    #         title = process_line(line, 'TITLE')[0]
    #         if strict_title_case:
    #             album.set_title(TitleCase(title))
    #         else:
    #             album.title = title
    #     elif line.startswith('FILE'):
    #         path = process_line(line, 'FILE', many=True)[0]
    #         last_idx = path.rfind(' ')
    #         if '.' in path[:last_idx]:
    #             path = path[:last_idx]
    #         current_file = path.strip('\'"')

    #     elif line.startswith('REM GENRE'):
    #         genre = process_line(line, 'REM GENRE')[0]
    #         if strict_title_case:
    #             album.rem.set_genre(TitleCase(genre))
    #         else:
    #             album.rem.genre = genre
    #     elif line.startswith('REM DATE'):
    #         album.rem.date = int(process_line(line, 'REM DATE')[0])
    #     elif line.startswith('REM REPLAYGAIN_ALBUM_GAIN'):
    #         album.rem.replaygain_album_gain = process_line(
    #             line, 'REM REPLAYGAIN_ALBUM_GAIN'
    #         )[0]
    #     elif line.startswith('REM REPLAYGAIN_ALBUM_PEAK'):
    #         album.rem.replaygain_album_peak = process_line(
    #             line, 'REM REPLAYGAIN_ALBUM_PEAK'
    #         )[0]

    #     elif line.startswith('TRACK'):
    #         if current_track:
    #             album.add_track(current_track)
    #         track = process_line(line, 'TRACK', many=True)[0].split()[0]
    #         current_track = TrackData(
    #             track=int(track), file=Path(current_file) if current_file else None
    #         )

    #     elif line.startswith('TITLE') and current_track:
    #         title = process_line(line, 'TITLE')[0]
    #         if strict_title_case:
    #             current_track.set_title(TitleCase(title))
    #         else:
    #             current_track.title = title
    #     elif line.startswith('PERFORMER') and current_track:
    #         performer = process_line(line, 'PERFORMER')[0]
    #         if strict_title_case:
    #             current_track.set_performer(TitleCase(performer))
    #         else:
    #             current_track.performer = performer
    #     elif line.startswith('INDEX 00') and current_track:
    #         idx = process_line(line, 'INDEX 00')[0]
    #         current_track.index00 = idx
    #     elif line.startswith('INDEX 01') and current_track:
    #         idx = process_line(line, 'INDEX 01')[0]
    #         current_track.index01 = idx

    # if current_track:
    #     album.add_track(current_track)

    return album
