from pathlib import Path
from typing import Iterator
from cuetools.models import AlbumData
from cuetools.parser.errors import CueParseError, CueValidationError
from cuetools.parser.handlers import title_case_handler
from cuetools.parser.lex import Token, lex


def load_f_iter(cue: Iterator[str], strict_title_case: bool = False) -> AlbumData:
    """loading an object from an iterator"""
    album = AlbumData()
    # current_track = None
    current_file = None  # type: ignore

    current_line = 0

    for line in cue:
        current_line += 1
        tokens = [i for i in lex(line)]

        match tokens[0].type:
            case Token.PERFORMER:
                performer = tokens[1]
                title_case_handler(
                    performer,
                    strict_title_case,
                    lambda x: setattr(album, 'performer', x),
                    album.set_performer,
                    current_line,
                    line,
                    'album performer name',
                )
            case Token.TITLE:
                title = tokens[1]
                title_case_handler(
                    title,
                    strict_title_case,
                    lambda x: setattr(album, 'title', x),
                    album.set_title,
                    current_line,
                    line,
                    'album title',
                )
            case Token.FILE:
                filepath = tokens[1]
                match filepath.type:
                    case Token.ARG_QUOTES:
                        file_type = tokens[2]
                        match file_type.type:
                            case Token.WAVE:
                                if filepath.lexeme.endswith('.mp3'):
                                    raise CueParseError(
                                        current_line,
                                        line,
                                        'MP3',
                                        file_type.lexeme,
                                        file_type.pos,
                                    )
                            case _:
                                raise CueParseError(
                                    current_line,
                                    line,
                                    'file type tag',
                                    file_type.lexeme,
                                    file_type.pos,
                                )

                        current_file = (  # noqa: F841 # type: ignore
                            Path(filepath.lexeme),
                            current_line,
                            line,
                            filepath.pos,
                            filepath.lexeme,
                        )
                    case _:
                        CueParseError(
                            current_line,
                            line,
                            'audiofile path',
                            filepath.lexeme,
                            filepath.pos,
                        )
            case Token.REM:
                rem_type = tokens[1]
                match rem_type.type:
                    case Token.GENRE:
                        genre = tokens[2]
                        title_case_handler(
                            genre,
                            strict_title_case,
                            lambda x: setattr(album.rem, 'genre', x),
                            album.rem.set_genre,
                            current_line,
                            line,
                            'album genre',
                        )
                    case Token.DATE:
                        date = tokens[2]
                        try:
                            album.rem.date = int(date.lexeme)
                        except ValueError as e:
                            raise CueValidationError(
                                current_line, line, date.pos, date.lexeme, e
                            )
                    case _:
                        raise CueParseError(
                            current_line,
                            line,
                            'Correct REM parameter',
                            rem_type.lexeme,
                            rem_type.pos,
                        )

            case _:
                raise CueParseError(
                    current_line,
                    line,
                    'Correct CUE keyword',
                    tokens[0].lexeme,
                    tokens[0].pos,
                )

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
